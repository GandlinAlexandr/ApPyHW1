<a name="readme-top"></a>


[![MIT][license-shield]][license-url]
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[!['Black'](https://img.shields.io/badge/code_style-black-black?style=for-the-badge)](https://github.com/psf/black)

  <h1 align="center">Небольшой игрушечный проект по Streamlit</h1>

  <p align="center">
    Первый проект по Streamlit
  </p>


<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#о-проекте">О проекте</a>
        <li><a href="#технологии">Технологии</a></li>
    </li>
    <li>
      <a href="#содержание-проекта">Содержание проекта</a>
    </li>
    <ul>
    <li><a href="#шаг-1-загрузка-данных">Шаг 1: Загрузка данных</a></li>
    <li><a href="#шаг-2-получение-актуальных-данных">Шаг 2: Получение актуальных данных</a></li></ul>
      <li><a href="#лицензия">Лицензия</a></li>
    <li><a href="#контакты">Контакты</a></li>
  </ol>
</details>



### О проекте

Представляет собой игрушечный проект по визуализации данных по температурам в разных городах.

## Технологии

Для реализации проекта использовались следующие технологии:

* [![Python][Python.org]][Python-url]
  * [![Matplotlib][Matplotlib.org]][Matplotlib-url]
  * [![Numpy][Numpy.org]][Numpy-url]
  * [![Pandas][Рandas.pydata.org]][Pandas-url]
  * [![Seaborn][Seaborn-badge]][Seaborn-url]
  * [![Streamlit][StreamlitBadge]][Streamlit-url]


<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Содержание проекта

Содержит простое streamlit-приложение.

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


### Шаг 1: Загрузка данных

Требуется загрузить датасет с историческими данным по температурам для разных городов и сезонов на протяжении нескольких лет. В ответ отобразится статистика по температурам.
Структура датасета:

|          city         | timestamp     |     temperature  |     season       |
|-----------------------|---------------|------------------|------------------|
|    New York           |    01.01.201|-5.83282310497167    |      winter       |

[Пример датасета](https://github.com/GandlinAlexandr/ApPyHW1/blob/main/temperature_data.csv) (искусственные данные).

После загрузки для выбранного города выводятся описательные статистики, в том числе по сезонам. Выводятся динамика температур на основании скользящих средних (с размером рамки 30), а также выделяются аномальные данные, выходящие за пределы двух стандартных отклонений от скользящего среднего.

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


### Шаг 2: Получение актуальных данных

Загружается API-ключ сервиса [OpenWeatherMap](https://openweathermap.org/api). В ответ выводит текущие погодные условия для города, выбранного из представленных в загруженном датасете. Также определяется, является ли текущая температура в городе с учётом сезона аномальной или нет. Определяется на основе загруженных данных на основании средней температуры за сезон.

Эта опция доступна только после загрузки датасета с историческими данными.

Ссылка на [streamlit-приложение](https://appyhw1-6csvzbjcb3ecafj3xa5bq6.streamlit.app/).


<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Лицензия

Распространяется по лицензии MIT. Дополнительную информацию см. в файле `LICENSE`.

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

## Контакты

Гандлин Александр - [Stepik](https://stepik.org/users/79694206/profile)

Ссылка на проект: [https://github.com/GandlinAlexandr/ApPyHW1](https://github.com/GandlinAlexandr/ApPyHW1)

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>


[license-shield]: https://img.shields.io/github/license/GandlinAlexandr/ApPyHW1.svg?style=for-the-badge
[license-url]: https://github.com/GandlinAlexandr/NLP_project/blob/main/LICENSE

[Python-url]: https://python.org/
[Python.org]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue

[Pandas-url]: https://pandas.pydata.org/
[Рandas.pydata.org]: https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white

[Numpy-url]: https://numpy.org/
[Numpy.org]: https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white

[Matplotlib-url]: https://matplotlib.org/
[Matplotlib.org]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black

[StreamlitBadge]: https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/

[Seaborn-url]: https://seaborn.pydata.org/
[Seaborn-badge]: https://img.shields.io/badge/Seaborn-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=blue
