<div id="top"></div>
<!-- PROJECT SHIELDS -->
<!--
*** See the bottom of this document for the declaration of the reference variables
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br>
<div align="center">
  <a href="https://github.com/earthdaily">
    <img src="https://earthdaily.com/hubfs/EDA_logo_horizontal_gradient-navy_1.svg"  alt="Logo" width="400" height="200">
  </a>
  
  <h1>Earthdaily Product documentation</h1>

  <p>
    Learn how to use Earthdaily platform capabilities within your business workflows! Cloud-native Earth observation with trusted data, flexible analytics, and seamless API integration.
  </p>

  <p>
    <a href="https://github.com/earthdaily/reflectance-datacube-processor/issues">Report Bug</a>
    ·
    <a href="https://github.com/earthdaily/reflectance-datacube-processor/issues">Request Feature</a>
  </p>
</div>

<div align="center"></div>

<div align="center">
  
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]
[![Youtube][youtube-shield]][youtube-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  
- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisite](#prerequisite)
  - [Installation](#installation)
- [Usage](#usage)
  - [Run website locally](#Run-site-locally)
  - [Provide content](#lContribute-to-documentation )
- [Resources](#resources)
- [Support development](#support-development)
- [License](#license)
- [Contact](#contact)
- [Copyrights](#copyrights)

</details>

<!-- ABOUT THE PROJECT -->
## About The Project

</p> Goal of this project is to provide user friendly on how to use, integrate Earthdaily services. It contains a broad set of ressouces allowing end users and integrators to leverage our services and analytics. </p>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisite

 <p align="left">

To be able to run this project locally , you will need to have following tools installed:

1. Install Conda: please install Conda on your computer. You can download and install it by following the instructions provided on the [official Conda website](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

2. Install Git: please install Github on your computer. You can download and install it by visiting <a href=<https://desktop.github.com/>here></a> and following the provided instructions

This project has been tested on Python 3.11

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation

To set up this project, follow these steps:

1. Clone the project repository:

    ```
    git clone https://github.com/earthdaily/earthdaily-documentation
    ```

2. Create the required Conda environment:

    ```
    conda create --name documentation python=3.11
    ```

3. Activate the Conda environment:

    ```
    conda activate documentation
    ```

4. Install mkdocs-material:

    ```
    pip install mkdocs-material
    ```
5. Navigate to the local project folder

    ```
    cd <path to project folder>
    ```
6. Intall dependencies from requirement.txt

    ```
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->
## Usage

### Run site locally

To run the website locally, you use the following command:

1. Open a terminal in the project folder.

2. Activate the Conda environment:

    ```
    conda activate documentation
    ```

3. Serve locally:

    ```
    mkdocs serve
    ```

4. Open your browser 

    ```
    http://127.0.0.1:8000/documentation/
    ```

### Contribute to documentation 
To create new pages, just add new markdown files to the [docs folder] of the repository and edit them.  
MkDocs will then turn those into static HTML pages once you [build](#build-pages) or [deploy](#deploy-to-github) the pages.

### Update content
If you are usingd VS code to update content please open site folder. Once done, you will benefit from auto completion and image preview.

<p align="right">(<a href="#top">back to top</a>)</p>

## Deploy to GitHub page
A deployment workflow has been configured to build and deploy website on each commit to main branch.

This workflow will setup Python, download Material for MkDocs and all its dependencies and deploy the pages to the `gh-pages` branch to then be viewable under this [URL](https://earthdaily.github.io/earthdaily-documentation/).

### Dependabot

The repository contains a `dependabot.yml` file inside the `.github` folder which allows automatic updates through GitHub's Dependabot.  

It is configured to target both Python dependencies (inside the `requirements.txt`) and GitHub Actions dependencies, to make sure bot are updated accordingly.

Note that it is configured by default to add the `Type: Update (Dependency)` label and also the `Target: Python (pip)` label for Python and `Target: GitHub Actions` label for GitHub Actions Dependencies.  

Those labels don't exist by default so you have to either create them, or alter the ones in the dependabot.yml (You can also just remove the `labels` sections).

<!-- RESOURCES -->
## Resources

The following links will provide access to more information:

- [Markdown foundations](https://www.markdownguide.org/basic-syntax/#reference-style-links)
- [Mkdocs]
- [Mkdocs Material][squidfunk]
- [Examples]()

**Tips** To generate folder structure with ASCII characters, you can use the command 'tree".
   - Open the Command Prompt (Start button + type "cmd").
   - Navigate to the desired root directory using the cd command. For example, to go to C:\MyDocuments
   - Execute the tree command with the /f and /a switches, redirecting the output to a text file. The /f switch displays the names of files in each folder, and /a uses ASCII characters for the tree structure:    `tree /f /a > FolderStructure.txt`



<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Support development

If this project has been useful, that it helped you or your business to save precious time, don't hesitate to give it a star.

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the [MIT License](https://github.com/GEOSYS/earthdaily-data-processor/blob/main/LICENSE).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

For any additonal information, please [email us](mailto:sales@earthdailyagro.com).

<p align="right">(<a href="#top">back to top</a>)</p>

## Copyrights

© 2025 Geosys Holdings ULC, an Antarctica Capital portfolio company | All Rights Reserved.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- List of available shields https://shields.io/category/license -->
<!-- List of available shields https://simpleicons.org/ -->
[issues-shield]: https://img.shields.io/github/issues/GEOSYS/earthdaily-data-processor/repo.svg?style=social
[issues-url]: https://github.com/GEOSYS/earthdaily-data-processor/issues
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=social&logo=linkedin
[linkedin-url]: https://www.linkedin.com/company/earthdailyagro/mycompany/
[twitter-shield]: https://img.shields.io/twitter/follow/EarthDailyAgro?style=social
[twitter-url]: https://img.shields.io/twitter/follow/EarthDailyAgro?style=social
[youtube-shield]: https://img.shields.io/youtube/channel/views/UCy4X-hM2xRK3oyC_xYKSG_g?style=social
[youtube-url]: https://img.shields.io/youtube/channel/views/UCy4X-hM2xRK3oyC_xYKSG_g?style=social
[docs folder]: https://github.com/Andre601/mkdocs-template/blob/master/docs
[MkDocs]: https://www.mkdocs.org/
[squidfunk]: https://github.com/squidfunk
[MkDocs Material Theme]: https://github.com/squidfunk/mkdocs-material
____________________________________________________

[use]: https://github.com/Andre601/mkdocs-template/generate
[facelessuser]: https://github.com/facelessuser
[PyMdown Extensions]: https://github.com/facelessuser/pymdown-extensions/




