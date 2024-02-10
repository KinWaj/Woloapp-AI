<div align="center" width="200" height="auto" >
     <img src="img/logo.svg">
    <h1> Woloapp-AI </h1 >
    AI support for Web Application for Regional Volunteer Centre in Gdańsk, which helps volunteers find and partake in events.
</div>

## ⚙️ Running the aplication

### Run application with Flask
>[!NOTE] 
>To start the application, make sure to run [WoloApp API](https://github.com/yarpo/wolo-app-api) first.

From the Woloapp-AI directory run:

    python -m flask --app ./app/app.py run

## 🤖 Used Models
- [ayakiri/wolo-app-categories-setfit-model](https://huggingface.co/ayakiri/wolo-app-categories-setfit-model)
- [facebook/mbart-large-50-many-to-many-mmt](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt)
- [microsoft/git-base-coco](https://huggingface.co/microsoft/git-base-coco)
- [IMSyPP/hate_speech_en](https://huggingface.co/IMSyPP/hate_speech_en)

<details>
<summary><h2>🧰 Used Technologies</h2></summary>
<ul>
<li>Python
<li>Pylint
<li>Flask
<li>Transformers
<li>PyTorch
<li>Sentencepiece
<li>Setfit
<li>Protobuf
<li>Flask-CORS
<li>Requests
<li>Pillow
</ul>
</details>


## 👋 Contributors
- [@MKurshakova](https://github.com/MKurshakova)
- [@Agata Dobrzyniewicz](https://github.com/ayakiriya)
- [@Kinga](https://github.com/KinWaj)
- [@Filiposki54](https://github.com/Filiposki54)

## Related Repositories
- [WoloApp](https://github.com/yarpo/wolo-app/)
- [WoloApp API](https://github.com/yarpo/wolo-app-api/)
