# appgenpro

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## DESCRIPTION
Transforming Application Development with appgenpro

In the rapidly evolving landscape of Generative AI, the leap into coding can be daunting. Traditional interfaces, like ChatGPT, often require specific know-how, turning the process of developing useful applications into a time-consuming task. 

Imagine ChatGPT as an eager yet inexperienced junior developer - enthusiastic and skilled in coding basics, but often unsure about navigating the complexities of application development.


Enter appgenpro - your solution to these challenges!

**For Non-Technical Business Professionals:**

- User-Friendly Interface: With appgenpro's chat interface, simply share your application idea, and watch as it orchestrates the entire development lifecycle for you. It's like having a virtual development team at your fingertips, tailored to your project's needs based on pre-set standards.
- Intuitive Collaboration: Our AI agents, skilled in asking the right questions, will guide you through the process. They seek your feedback to refine outputs, making assumptions to ease your journey if you're not technically inclined.
- Comprehensive Deliverables: From requirements and design documents to functional code and deployment artifacts, appgenpro covers it all. Your final application can be seamlessly pushed to GitHub or deployed to cloud platforms like render.com.


**For Developers and Technical Experts:**

- Command Line Efficiency: Dive into the full development cycle with a command-line interface, fine-tune standards, and iterate on deliverables for that perfect touch.
- End-to-End Capability: Push your polished code directly to GitHub and deploy to any cloud service, streamlining your workflow.


**Embracing Challenges and Future Vision:**

- While appgenpro excels in creating a variety of applications, we recognize the current limitations in generating complex UI code with LLMs. Rest assured, our upcoming releases are focused on enhancing these capabilities, especially in backend development areas like APIs, microservices, BI solutions, and AI applications.
- Our virtual development team is powered by specialized AI agents that are continually evolving. We're committed to enabling them to learn from their experiences, gaining domain expertise to further enrich and expedite the development process.


**Join Our Journey:**

As we progress along our roadmap, we invite the community to share their ideas and suggestions. Your input is invaluable in shaping appgenpro to be more versatile, user-friendly, and innovative. Together, let's redefine the frontiers of application development!


https://github.com/datanomous-uk/appgenpro/assets/46131251/3396a2c4-9aa7-464e-9109-b2d45a00d8f1



## TABLE OF CONTENTS

- [Setup](#SETUP)
- [Usage](#USAGE:For_technical_experts)
- [Usage](#USAGE:For_non-technical_users)
- [Contact](#CONTACT)
- [Citiations](#CITATIONS)


Please see `ROADMAP.md` for details of the aim of appgenpro and our mission.

Please see `DEV.md` for details on dev topics and troubleshooting tips.

Please see `CONFIG.md` for details on how to configure appgenpro.

Please see `CONTRIBUTIONS.md` for details on how to contribute to our journey.




## SETUP

To get started with AppGenPro, follow these steps:

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

4. Configure `appgenpro_config.yaml` 
* Validate the `mmdc` path by typing `ls ./node_modules/.bin/mmdc` in the terminal.
* Update `OAI_CONFIG_LIST` and `GITHUB_TOKEN` for OpenAPI model/key and to use github.



# USAGE:For_technical_experts

To use appgenpro, you can either run it via the command line or through a Chat UI:

1. **Command Line: Run Full Application Lifecycle**

```shell
python appgenpro_cli.py --idea "Type your app idea..." -- config f"{EXAMPLES_ROOT}/flask_app/app_implement_only_config.json" --name "flask_app"
```

1.1 **Command Line: Run Iterative Application Lifecycle with the available Requirements and Design Documents** 

```shell
python appgenpro_cli.py --config 'examples/flask_app/app_config_implement_only.json' --idea 'Create an application with secure API endpoints only that enables admin users to create advanced dynamic forms and users to fill them in. Store the data in database.' --name 'flask_app' --backlog 'flask_app/docs/backlog.md'
```

1.2 **Command Line: Run Iterative Application Lifecycle with the available Requirements and Design Documents and Github Token to push the generated code**
```shell
python appgenpro_cli.py --config 'examples/flask_app/app_config_implement_only.json' --idea 'Create an application with secure API endpoints only that enables admin users to create advanced dynamic forms and users to fill them in. Store the data in database.' --name 'flask_app' --github_token 'your_github_token' --backlog 'flask_app/docs/backlog.md'

```

1.3 **Command Line: Or see options to decide **

```shell
python appgenpro_cli.py --help
```




# USAGE:For_non-technical_users

1. **Chat UI: Run Full Application Lifecycle**

Update the `appgenpro_chat_config.json` with the target application specifics

Run AppGenPro with a Chat UI for an enhanced user experience:

```shell
chainlit run appgenpro_chat.py 
```






# CONTACT
If you have any questions or feedback, feel free to reach out to us:

* [Email](mailto:improve.appgenpro@gmail.com?subject=[GitHub]%20appgenpro%20query)







# CITATIONS
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