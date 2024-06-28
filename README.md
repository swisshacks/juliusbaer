<p align="center">
  <img src="./swisshacks-logo.png" width="300">
</p>

# SwissHacks 2024 - Using AI against Deepfakes Challenge
Welcome to the "Using AI against Deepfakes" Challenge. This README leads you through this challenge and contains all the relevant information. In case something is unclear don't hesitate to get in touch with us.

## Motivation
We are tackling the challenge of identifying real and fake audio recordings in phone calls between clients and Relationship Managers (RMs) because we want to ensure the highest level of security and trust in our bank's services. With the rise of advanced AI and deepfake audio, the risk of fraud and identity theft has grown, threatening both our clients and our operations. By creating effective ways to tell apart real and fake recordings, check if the information shared matches the client's profile, and spot human impersonators, we aim to strengthen our protection against fraud. This effort helps make our services safer and more reliable, showing our commitment to protecting our clients' financial and personal information.

## Your Task
In this challenge, you will need to create solutions that can tell apart real and fake audio recordings of clients. You will develop tools to check if the information shared in these calls matches the client's profile. Additionally, you will need to figure out if a human voice in the recording is the actual client or an impersonator. We will provide you with a set of client profiles each with one verified authentic sample of the client's voice. Furthermore, you will receive the labels for a subset of the dataset and we expect you to provide the labels for the remaining audio clips (more details follow below).

## Audio Dataset
You will get 400 audio recordings from 20 different clients, along with the profiles of those 20 clients. For each client, we have labeled one recording as original/true and one as AI-generated. Every audio recording (original or fake) contains the correct client name. Your task is to classify the rest of the recordings as:

- Original (real human speaking) or fake (AI-generated).

- Factually consistent or factually inconsistent with the client profile. For example, if the client profile says the person is married but the recording says they are single, that is factually inconsistent.

- If it is a human speaking, determine if it is the real client or an impersonator.

Beware, most of the recordings are in English, but some are in other languages like Italian or French.

## Tips
### Analyze The Data
Before you start building your awesome audio labeler, analyze the sample data properly and ask yourself fundamental questions about the problem structure. Can you manually identify the labels yourself? Which labels are low-hanging fruits and should be prioritized?

### Handy Tools & Concepts
There are many tools out there that can do a lot of the heavy lifting for you. For text processing, already the built-in regex library of Python goes a long way. Take also a look at tools like [nltk](https://www.nltk.org/) that can do things like [Named Entity Recognition (NER)](https://medium.com/mysuperai/what-is-named-entity-recognition-ner-and-how-can-i-use-it-2b68cf6f545d). For audio preprocessing, check out the Python audio library [Librosa](https://librosa.org/). There is also a helpful blog series about voice computing where you can learn the basics about the topic ([1](https://maelfabien.github.io/machinelearning/Speech8/), [1](https://maelfabien.github.io/machinelearning/Speech9/), [3](https://maelfabien.github.io/machinelearning/Speech10/)). Get some inspiration how other people built audio classifiers with [GradientBoosting models](https://www.geeksforgeeks.org/audio-classification-using-spectrograms/) or [CNNs](https://towardsdatascience.com/audio-deep-learning-made-simple-sound-classification-step-by-step-cebc936bbe5).

### Divide & Conquer
To tackle this challenge, try breaking it into smaller tasks. First, identify if an audio recording is real or fake. Then, check if the information matches the client’s profile. Finally, determine if the human voice is the real client or an impersonator. Combining these steps into a pipeline will help you create an effective solution.

## Rating System
### Prediction Score
For classifying true or fake audio recordings, there are a total of 360 points available (1 point for each correct classification).
For classifying factual correctness or incorrectness, there are 380 points available (1 point for each correct classification). Among the 20 audios labeled from the real client, there are no factual inconsistencies, leaving 380 points (400 - 20 = 380).
Additionally, correctly identifying whether a human voice belongs to the real client or an impersonator earns an additional point when the audio is real.
Your total points will be converted into a score from 0 to 50, using a linear conversion. Achieving the maximum points gives a score of 50. This score accounts for 50% of your final score.

### Solution Score
Your solution will be evaluated based on criteria like efficiency, novelty, elegance and applicability within the banking sector with a potential score ranging from 0 to 50.
This score also contributes 50% to your final score.

### Final Score
Your final score is calculated as the sum of your Prediction Score and Solution Score, ranging from 0 to 100.

### Hand-in
To evaluate your prediction score, we need your classification labels in the same format as in the provided example. The order in which you list the audios doesn't matter. Please, name your submission csv file as "<team_name>.csv". Please fork this repository, start developing your project, and ensure your final submission, including your code, is uploaded to your forked repository, as this will be used to evaluate your solution.


**<team_name>.csv Example**
```
rec_id, is_fake, is_factually_correct, is_impersonator
656QZ2VWR4, True, False, False
WGTMM9VP8Z, True, True, True
56K4DSESF, False, False, True
...
```
