# ELTEA17
Entity-Level Tweets Emotion Analysis Dataset


Distribution of annotated data in sentence-level, over Ekman classes
![GitHub Logo](images/Sent_Anno_Distro.png)


## Annotation
This dataset has both sentence-level and token-level annotation. In the sentence-level annotation, each sentence is annotated with one of the six Ekman's classes. In the token-level an- notation, the annotation indicates each lexicon for their role (i.e., emotion holder, cause and target), plus emotion keywords.
```json
    {
        "emotion": "fea",
        "text": "I need a chemistry tutor because this is blowing me",
        "sarcasm": "N",
        "sent_num": "305"
    },
```

Tokens/Tags|I|need|a|tutor|because|**chemistry**|**exam**|is|**killing**|**me**
-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------
Anger|O-AN|O-AN|O-AN|O-AN|O-AN|O-AN|O-AN|O-AN|O-AN|O-AN
Disgust|O-DI|O-DI|O-DI|O-DI|O-DI|O-DI|O-DI|O-DI|O-DI|O-DI
Fear|O-FE|O-FE|O-FE|O-FE|O-FE|O-FE|O-FE|O-FE|**B-FE**|O-FE
Sadness|O-SA|O-SA|O-SA|O-SA|O-SA|O-SA|O-SA|O-SA|**B-SA**|O-SA
Surprise|O-SU|O-SU|O-SU|O-SU|O-SU|O-SU|O-SU|O-SU|O-SU|O-SU
Joy|O-JO|O-JO|O-JO|O-JO|O-JO|O-JO|O-JO|O-JO|O-JO|O-JO
Holder|O-EH|O-EH|O-EH|O-EH|O-EH|O-EH|O-EH|O-EH|O-EH|**B-EH**
Cause|O-EC|O-EC|O-EC|O-EC|O-EC|**B-EC**|**I-EC**|O-EC|O-EC|O-EC
Target|O-ET|O-ET|O-ET|O-ET|O-ET|O-ET|**B-ET**|O-ET|O-ET|O-ET


## Citation
For academic usage please cite the following pre-print
[Structured Emotion Prediction of Tweets With Co-extraction of Cause, Holder and Target of Emotions](https://www.researchgate.net/profile/Roozbeh-Bandpey-2/publication/341344305_Structured_Emotion_Prediction_of_Tweets_With_Co-extraction_of_Cause_Holder_and_Target_of_Emotions/links/5ebbc08ea6fdcc90d6728396/Structured-Emotion-Prediction-of-Tweets-With-Co-extraction-of-Cause-Holder-and-Target-of-Emotions.pdf)

Bib format
```bib
@PrePrint{Bandpey,
  author    = {Roozbeh Bandpey},
  title     = {Structured Emotion Prediction of Tweets With Co-extraction of Cause, Holder and Target of Emotions},
  booktitle = {Structured Emotion Prediction of Tweets With Co-extraction of Cause, Holder and Target of Emotions. pages 15-25. ResearchGate},
  year      = {2017}
}
```