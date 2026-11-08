from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-for-production'
WORDS = {
    'Animals': ['ELEPHANT', 'GIRAFFE', 'DOLPHIN', 'PENGUIN', 'KANGAROO', 'CHEETAH'],
    'Technology': ['PYTHON', 'KEYBOARD', 'INTERNET', 'DATABASE', 'ALGORITHM', 'COMPUTER'],
    'Nature': ['MOUNTAIN', 'RAINBOW', 'FOREST', 'WATERFALL', 'SUNFLOWER', 'OCEAN'],
    'Food': ['CHOCOLATE', 'SANDWICH', 'PANCAKE', 'BIRYANI', 'STRAWBERRY', 'NOODLES']
}
HINTS = {
    'ELEPHANT':'A large animal with a trunk.', 'GIRAFFE':'The tallest land animal.', 'DOLPHIN':'A clever sea mammal.',
    'PENGUIN':'A bird that cannot fly and loves cold places.', 'KANGAROO':'An Australian animal that hops.', 'CHEETAH':'The fastest land animal.',
    'PYTHON':'A popular programming language.', 'KEYBOARD':'You use it to type.', 'INTERNET':'A worldwide network of computers.', 'DATABASE':'An organized collection of information.', 'ALGORITHM':'A step-by-step method to solve a problem.', 'COMPUTER':'An electronic device for processing data.',
    'MOUNTAIN':'A very high natural landform.', 'RAINBOW':'A colorful arc after rain.', 'FOREST':'A large area covered with trees.', 'WATERFALL':'Water flowing over a steep edge.', 'SUNFLOWER':'A yellow flower that follows the sun.', 'OCEAN':'A very large body of salt water.',
    'CHOCOLATE':'A sweet treat made from cocoa.', 'SANDWICH':'Food served between slices of bread.', 'PANCAKE':'A flat breakfast food cooked in a pan.', 'BIRYANI':'A spiced rice dish.', 'STRAWBERRY':'A red fruit with tiny seeds outside.', 'NOODLES':'Long thin strips of pasta.'
}

def new_game(category=None):
    category = category if category in WORDS else random.choice(list(WORDS))
    word = random.choice(WORDS[category])
    session.update(word=word, category=category, guessed=[], wrong=[], won=False, lost=False)
    return state()

def state():
    word = session.get('word', 'PYTHON')
    guessed = session.get('guessed', [])
    wrong = session.get('wrong', [])
    won = all(ch in guessed for ch in set(word))
    lost = len(wrong) >= 6 and not won
    session['won'], session['lost'] = won, lost
    return {'word': word, 'display': ' '.join(ch if ch in guessed else '_' for ch in word),
            'guessed': guessed, 'wrong': wrong, 'mistakes': len(wrong), 'remaining': 6-len(wrong),
            'category': session.get('category'), 'hint': HINTS.get(word, 'Guess the hidden word!'),
            'won': won, 'lost': lost, 'game_over': won or lost}

@app.route('/')
def index():
    if 'word' not in session: new_game()
    return render_template('index.html', categories=list(WORDS))

@app.route('/api/state')
def get_state(): return jsonify(state())

@app.route('/api/new', methods=['POST'])
def restart():
    category = (request.json or {}).get('category')
    return jsonify(new_game(category))

@app.route('/api/guess', methods=['POST'])
def guess():
    data = request.json or {}
    letter = str(data.get('letter', '')).upper()
    if len(letter) != 1 or not letter.isalpha(): return jsonify({'error':'Please choose a letter.'}), 400
    if session.get('won') or session.get('lost'): return jsonify(state())
    guessed = session.get('guessed', [])
    wrong = session.get('wrong', [])
    if letter not in guessed and letter not in wrong:
        if letter in session.get('word', ''): guessed.append(letter)
        else: wrong.append(letter)
    session['guessed'], session['wrong'] = guessed, wrong
    return jsonify(state())

if __name__ == '__main__':
    app.run(debug=True)
