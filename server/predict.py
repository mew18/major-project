import pickle
import matplotlib.pyplot as plt
import numpy as np

from keras.applications.inception_v3 import preprocess_input
from keras.models import load_model
from keras.preprocessing import image, sequence

model = load_model('server/utils/model.h5')
inception_v3 = load_model('server/utils/InceptionV3.h5')
# incept_model = InceptionV3(weights='imagenet')
# model_new = Model(incept_model.input, incept_model.layers[-2].output)
max_length=38 
test_img_path = 'client/test_img.jpg'

with open('server/utils/objs.pkl', 'rb') as f:
    ixtoword, wordtoix = pickle.load(f)

def beam_search_predictions(image, beam_index=3):
    start = [wordtoix["startseq"]]
    start_word = [[start, 0.0]]
    while len(start_word[0][0]) < max_length:
        temp = []
        for s in start_word:
            par_caps = sequence.pad_sequences(
                [s[0]], maxlen=max_length, padding='post')
            preds = model.predict([image, par_caps], verbose=0)
            word_preds = np.argsort(preds[0])[-beam_index:]
            # Getting the top <beam_index>(n) predictions and creating a
            # new list so as to put them via the model again
            for w in word_preds:
                next_cap, prob = s[0][:], s[1]
                next_cap.append(w)
                prob += preds[0][w]
                temp.append([next_cap, prob])

        start_word = temp
        # Sorting according to the probabilities
        start_word = sorted(start_word, reverse=False, key=lambda l: l[1])
        # Getting the top words
        start_word = start_word[-beam_index:]

    start_word = start_word[-1][0]
    intermediate_caption = [ixtoword[i] for i in start_word]
    final_caption = []

    for i in intermediate_caption:
        if i != 'endseq':
            final_caption.append(i)
        else:
            break

    final_caption = ' '.join(final_caption[1:])
    return final_caption

def predict():
    # pic = plt.imread(test_img_path)
    # plt.imshow(pic)
    # plt.show()

    test_jpg = image.load_img(test_img_path, target_size=(299, 299))
    test_jpg = image.img_to_array(test_jpg)
    test_jpg = np.expand_dims(test_jpg, axis=0)
    test_jpg = preprocess_input(test_jpg)
    test_jpg = inception_v3.predict(test_jpg)

    print("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-")
    print(test_jpg)
    
    # print("Beam Search, K = 3:", beam_search_predictions(test_jpg, beam_index=3))
    try:
        output = beam_search_predictions(test_jpg, beam_index=5)
        print(output)
    except:
        output = "Error! , please try again."
    # print("Beam Search, K = 7:", beam_search_predictions(test_jpg, beam_index=7))
    return output


if __name__ == '__main__':
    predict()
