from deep_translator import GoogleTranslator

from kickstarter_predictor.data import load_data

data = load_data(True, False, False, False)

sentence_samples = data.sample(20)['X']

translator = GoogleTranslator(source="auto", target="en")

translations = translator.translate_batch(list(sentence_samples.values))

print(translations)