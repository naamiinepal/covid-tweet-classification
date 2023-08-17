# COVID-19-related Nepali Tweets Classification in a Low Resource Setting

by
Rabin Adhikari,
Safal Thapaliya,
Nirajan Basnet,
Samip Poudel,
Aman Shakya,
Bishesh Khanal

This repository contains the data and source code used to produce the results presented in the
[The Seventh Workshop on Social Media Mining for Health Applications, Workshop & Shared Task 2022 (#SMM4H)](https://healthlanguageprocessing.org/smm4h-2022/).

## Abstract

Billions of people across the globe have been using social media platforms in their local languages to voice their opinions about the various topics related to the COVID-19 pandemic.
Several organizations, including the World Health Organization, have developed automated social media analysis tools that classify COVID-19-related tweets into various topics.
However, these tools that help combat the pandemic are limited to very few languages, making several countries unable to take their benefit.
While multi-lingual or low-resource language-specific tools are being developed, there is still a need to expand their coverage, such as for the Nepali language.
In this paper, we identify the eight most common COVID-19 discussion topics among the Twitter community using the Nepali language, set up an online platform to automatically gather Nepali tweets containing the COVID-19-related keywords, classify the tweets into the eight topics, and visualize the results across the period in a web-based dashboard.
We compare the performance of two state-of-the-art multi-lingual language models for Nepali tweet classification, one generic (mBERT) and the other Nepali language family-specific model (MuRIL).
Our results show that the models’ relative performance depends on the data size, with MuRIL doing better for a larger dataset.
The annotated data, models, and the web-based dashboard are open-sourced [here](https://github.com/naamiinepal/covid-tweet-classification).

## Link to Paper

The paper is found at https://aclanthology.org/2022.smm4h-1.52/

## Citation

Please cite the paper and data used as follows:

> Rabin Adhikari, Safal Thapaliya, Nirajan Basnet, Samip Poudel, Aman Shakya, and Bishesh Khanal. 2022. [COVID-19-related Nepali Tweets Classification in a Low Resource Setting](https://aclanthology.org/2022.smm4h-1.52). In _Proceedings of The Seventh Workshop on Social Media Mining for Health Applications, Workshop & Shared Task_, pages 209–215, Gyeongju, Republic of Korea. Association for Computational Linguistics.

For the biblatex version:

```bib
@inproceedings{adhikari-etal-2022-covid,
    title = "{COVID}-19-related {N}epali Tweets Classification in a Low Resource Setting",
    author = "Adhikari, Rabin  and
      Thapaliya, Safal  and
      Basnet, Nirajan  and
      Poudel, Samip  and
      Shakya, Aman  and
      Khanal, Bishesh",
    booktitle = "Proceedings of The Seventh Workshop on Social Media Mining for Health Applications, Workshop {\&} Shared Task",
    month = oct,
    year = "2022",
    address = "Gyeongju, Republic of Korea",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.smm4h-1.52",
    pages = "209--215",
}
```

## License

All Python source code (including `.py` and `.ipynb` files) is available under the MIT license.
You can use and modify the code without warranty if you give attribution to the authors.
See [LICENSE](LICENSE) for the full license text.

## Deployment
The server is deployed at https://covid-talks.naamii.org.np/.

|  | Build Status |
|-:|:-----|
| Client Side | [![React Move Build to Server](https://github.com/rabinadk1/EpiSuS/actions/workflows/build-to-server.yml/badge.svg)](https://github.com/rabinadk1/EpiSuS/actions/workflows/build-to-server.yml) |
| Server Side | [![Backend Code Coverage](https://codecov.io/gh/rabinadk1/EpiSuS/branch/main/graph/badge.svg?token=CBU0VJDGYS)](https://codecov.io/gh/rabinadk1/EpiSuS) |
