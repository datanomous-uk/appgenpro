# aipreneuros

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-8A2BE2)](https://datanomous-uk.github.io/appgenpro-docs)

<<<<<<< Updated upstream
## Description

Appgenpro stands as a groundbreaking tool tailored for non-technical business professionals, enabling them to develop high-quality enterprise applications. This platform harnesses the capabilities of virtual "AI Agent" teams, each assigned to various roles in the application development process. These AI agents collaboratively work to produce outputs for each role, culminating in a functional business solution.

Appgenpro distinguishes itself from other similar open-source projects through its distinctive design, rooted in the autogen multi-agent framework, and its features specifically aimed at enterprise application development. As we diligently work to fulfill our roadmap, we invite the community to contribute suggestions for new features, enhancing the tool's utility and relevance for users. This collaborative approach ensures Appgenpro remains a cutting-edge and user-focused solution in the field of application development.
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Citations](#citations)
- [Contact](#contact)

Please see `ROADMAP.md` for details of the aim of aipreneuros and our mission.

Please see `DEV.md` for details on dev topics and troubleshooting tips.

Please see `CONFIG.md` for details on how to configure appgenpro.


## Installation

To get started with aipreneuros, follow these steps:

1. Create a Virtual Environment:
```shell
python3 -m venv myenv
source myenv/bin/activate
```

2. Install Python Dependencies:
```shell
pip install -r requirements.txt
```

3. Install Other Dependencies:
```shell
npm install @mermaid-js/mermaid-cli
```

<<<<<<< Updated upstream
4. Configuration:
* Navigate to `./appgen/config/config.yaml`.
=======
4. Configure `aipreneuros_config.yaml` 
>>>>>>> Stashed changes
* Validate the `mmdc` path by typing `ls ./node_modules/.bin/mmdc` in the terminal.
* Update `OAI_CONFIG_LIST` and `GITHUB_TOKEN` for OpenAPI model/key and to use github.

# Usage

<<<<<<< Updated upstream
To use appgenpro, you can either run it via the command line or through a Chat UI:

1. **Command Line:**

```shell
python appgenpro.py --idea "Type your app idea..."
```

For additional options, use:

```shell
python appgenpro.py --help
```

2. **Chat UI:**

Run AppGenPro using Chainlit for an enhanced user experience:

```shell
chainlit run appgenpro.py
```

# Contributing
We welcome contributions from the community! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

# License
This project is licensed under the MIT License. You can see the details in the LICENSE file.

# Citations
=======


# CONTACT
If you have any questions or feedback, feel free to reach out to us:

* [Email](mailto:improve.aipreneuros@gmail.com?subject=[GitHub]%20aipreneuros%20query)





# CITATIONS
>>>>>>> Stashed changes
We would like to acknowledge the use of external libraries and resources that have made this project possible.

Specifically,

[MetaGPT](https://github.com/geekan/MetaGPT/tree/main)
```
@misc{hong2023metagpt,
      title={MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework}, 
      author={Sirui Hong and Mingchen Zhuge and Jonathan Chen and Xiawu Zheng and Yuheng Cheng and Ceyao Zhang and Jinlin Wang and Zili Wang and Steven Ka Shing Yau and Zijuan Lin and Liyang Zhou and Chenyu Ran and Lingfeng Xiao and Chenglin Wu and Jürgen Schmidhuber},
      year={2023},
      eprint={2308.00352},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```
[AutoGen](https://github.com/microsoft/autogen/tree/main)
```
@inproceedings{wu2023autogen,
      title={AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework},
      author={Qingyun Wu and Gagan Bansal and Jieyu Zhang and Yiran Wu and Beibin Li and Erkang Zhu and Li Jiang and Xiaoyun Zhang and Shaokun Zhang and Jiale Liu and Ahmed Hassan Awadallah and Ryen W White and Doug Burger and Chi Wang},
      year={2023},
      eprint={2308.08155},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
```

# Contact
If you have any questions or feedback, feel free to reach out to us:

* [Email](mailto:improve.appgenpro@gmail.com?subject=[GitHub]%20appgenpro%20query)


