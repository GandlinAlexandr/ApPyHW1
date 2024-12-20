import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression


# Функция для получения текущей температуры по городу
def current_temperature(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {
            "cod": 401,
            "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.",
        }


# Функция для проверки аномальности температуры
def check_anomaly(city):
    temperature = current_temperature(city)["main"]["temp"]
    current_month = datetime.now().month
    if temperature is None:
        return None
    if current_month in [12, 1, 2]:
        season = "winter"
    elif current_month in [3, 4, 5]:
        season = "spring"
    elif current_month in [6, 7, 8]:
        season = "summer"
    else:
        season = "autumn"

    sd_season = df.loc[
        (df["city"] == city) & (df["season"] == season), "season_sd"
    ].iloc[0]
    season_mean = df.loc[
        (df["city"] == city) & (df["season"] == season), "season_mean"
    ].iloc[0]

    if (
        temperature < season_mean - 2 * sd_season
        or temperature > season_mean + 2 * sd_season
    ):
        return (
            f'<span style="color:red">*является аномальной*</span> для сезона {season}'
        )
    else:
        return f'<span style="color:green">*не является аномальной*</span> для сезона {season}'


def data_aggr(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(by="timestamp")
    df["moving_mean"] = df.groupby("city")["temperature"].transform(
        lambda x: x.rolling(window=30, min_periods=1).mean()
    )  # Расчет скользящего среднего
    df["moving_sd"] = df.groupby("city")["temperature"].transform(
        lambda x: x.rolling(window=30, min_periods=1).std()
    )  # Расчет скользящего стандартного отклонения
    df["season_mean"] = df.groupby(["city", "season"])["temperature"].transform(
        lambda x: x.mean()
    )  # Вычисление среднего
    df["season_sd"] = df.groupby(["city", "season"])["temperature"].transform(
        lambda x: x.std()
    )  # Вычисление стандартного отклонения
    df["is_anomaly"] = (df["temperature"] > df["moving_mean"] + 2 * df["moving_sd"]) + (
        df["temperature"] < df["moving_mean"] - 2 * df["moving_sd"]
    )  # Выявление аномалий
    df["lower_bound"] = df["moving_mean"] - 2 * df["moving_sd"]
    df["upper_bound"] = df["moving_mean"] + 2 * df["moving_sd"]
    return df


st.title("Анализ данных с использованием Streamlit")

st.header("Шаг 1: Загрузка данных")
uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])

if uploaded_file is not None:
    # Чтение CSV файла в pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Расчёты средних и отклонений
    df = data_aggr(df)

    # st.write("Превью данных:")
    # st.dataframe(df)

    # Убедитесь, что в DataFrame есть колонка 'city'
    if "city" in df.columns:
        # Создание выпадающего списка с городами
        selected_city = st.selectbox("Выберите город", sorted(df["city"].unique()))
        # Отображение выбранного города
        st.write(f"Вы выбрали город: {selected_city}")

        # Статистика
        st.subheader("Статистика")
        # Создание двух колонок
        st.write(
            f"Диапазон дат: {min(df[df['city'] == selected_city]['timestamp']).strftime('%d.%m.%Y')} "
            f"-- {max(df[df['city'] == selected_city]['timestamp']).strftime('%d.%m.%Y')}."
        )
        col1, col2 = st.columns(2)
        # Отображение таблиц в соответствующих колонках
        with col1:
            st.write("Полная статистика для температур города")
            st.dataframe(df[df["city"] == selected_city]["temperature"].describe())
        with col2:
            st.write("Статистика для температур по сезонам")
            st.dataframe(
                df[df["city"] == selected_city]
                .groupby(["season"])["temperature"]
                .describe()
                .T
            )

        # График
        st.subheader("Гистограмма распределения температур")
        bins = st.slider("Количество интервалов (bins)", 5, 50, 10)
        fig, ax = plt.subplots()
        sns.set_theme(style="darkgrid")
        ax.hist(df[df["city"] == selected_city]["temperature"], bins=bins)
        ax.set(title=f"{selected_city}", xlabel="Temperature, °C", ylabel="Count")
        st.pyplot(fig)

        st.subheader("Долгосрочная динамика температуры")
        fig, ax = plt.subplots(figsize=(8, 5))
        plt.fill_between(
            df[df["city"] == selected_city]["timestamp"],
            df[df["city"] == selected_city]["lower_bound"],
            df[df["city"] == selected_city]["upper_bound"],
            color="lightgrey",
            alpha=0.5,
        )
        sns.set_theme(style="darkgrid")
        lin = sns.lineplot(
            df[df["city"] == selected_city],
            x="timestamp",
            y="moving_mean",
            color="green",
            label="Rolling Mean",
        )
        dot = sns.scatterplot(
            df[df["city"] == selected_city],
            x="timestamp",
            y="temperature",
            hue="is_anomaly",
            palette={False: "gray", True: "red"},
            s=10,
        )
        ax.set(title=f"{selected_city}", xlabel="Date", ylabel="Temperature, °C")
        handles_sns, _ = dot.get_legend_handles_labels()
        # Объединяем легенды
        handles = [
            plt.Line2D([], [], color="lightgrey", alpha=0.5, linewidth=6)
        ] + handles_sns
        labels = ["±2 std dev", "rolling mean", "not anomaly", "anomaly"]
        # Устанавливаем объединённую легенду
        ax.legend(
            handles=handles, labels=labels, title=None, loc="lower left", fontsize=9
        )
        st.pyplot(fig)

        st.subheader("Boxplot для температур по сезонам")
        fig, ax = plt.subplots()
        sns.set_theme(style="darkgrid")
        sns.boxplot(
            df[df["city"] == selected_city],
            x="season",
            y="temperature",
            hue="season",
            showfliers=False,
        )
        ax.set(title=f"{selected_city}", xlabel="Season", ylabel="Temperature, °C")
        strip = sns.stripplot(
            df[df["city"] == selected_city],
            x="season",
            y="temperature",
            size=2.5,
            hue="is_anomaly",
            palette={False: "gray", True: "red"},
            alpha=0.3,
        )
        ax.legend_.remove()
        handles, labels = strip.get_legend_handles_labels()
        ax.legend(
            handles=handles,
            labels=["No", "Yes"],
            title="Anomaly",
            loc="upper left",
            fontsize=9,
        )
        st.pyplot(fig)

        st.subheader("Температурный тренд")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.set_theme(style="darkgrid")
        date_in_num = mdates.date2num(df[df["city"] == selected_city]["timestamp"])
        model = LinearRegression()
        model.fit(
            date_in_num.reshape(-1, 1), df[df["city"] == selected_city]["temperature"]
        )
        r_sq = model.score(
            date_in_num.reshape(-1, 1), df[df["city"] == selected_city]["temperature"]
        )
        sign = model.coef_[0] / abs(model.coef_[0])
        if sign > 0:
            st.markdown(
                f'r ≈ {round((r_sq ** 0.5) * sign, 5)}, тренд <span style="color:green">*положительный*</span>',
                unsafe_allow_html=True,
            )
        elif sign < 0:
            st.markdown(
                f'r ≈ {round((r_sq ** 0.5) * sign, 5)}, тренд <span style="color:red">*отрицательный*</span>',
                unsafe_allow_html=True,
            )

        sns.regplot(
            df[df["city"] == selected_city],
            x=date_in_num,
            y="temperature",
            scatter_kws={"s": 2.5},
            line_kws=dict(color="r"),
        )
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        ax.set(title=f"{selected_city}", xlabel="Date", ylabel="Temperature, °C")
        st.pyplot(fig)

        st.header("Шаг 2: Получение актуальных данных")

        api_key = st.text_input("Введите ваш API ключ OpenWeatherMap")

        if api_key:
            if current_temperature(selected_city)["cod"] == 200:
                st.subheader(f"Текущие погодные условия для города {selected_city}")
                weather = current_temperature(selected_city)
                st.markdown(
                    f"Дата: **{datetime.utcfromtimestamp(weather['dt']).strftime('%d.%m.%Y %H:%M')}**"
                )

                st.image(
                    f"http://openweathermap.org/img/wn/{weather['weather'][0]['icon']}.png",
                    width=50,
                )

                st.markdown(
                    f"Текущая температура: **{weather['main']['temp']}°C** {check_anomaly(selected_city)}",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"Текущее атмосферное давление: **{weather['main']['pressure']} гПа**"
                )
                st.markdown(f"Текущая влажность: **{weather['main']['humidity']}%**")
                st.markdown(f"Видимость: **{weather['visibility']} м**")
                st.markdown(f"Скорость ветра: **{weather['wind']['speed']} м/с**")
                st.markdown(f"Направление ветра: **{weather['wind']['deg']}°**")
                st.markdown(f"Покрытие облаками: **{weather['clouds']['all']}%**")
            else:
                st.write(current_temperature(selected_city))

    else:
        st.error("В загруженном файле нет столбца 'city'.")
