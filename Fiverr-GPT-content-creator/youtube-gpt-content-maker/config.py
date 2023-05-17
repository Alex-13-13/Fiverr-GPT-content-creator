
# MODEL SETTINGS
MODEL = "text-davinci-003"
API_PARAM = {
    'engine': MODEL,
    'max_tokens': 512,
    'temperature': 0.77,
    'top_p': 1,
    'frequency_penalty': 0.28,
    'presence_penalty': 0.13,
}
# VIDEO SETTINGS
CHANNEL_NAME = 'Motivation55'

### Duration should be the video length
# DURATION = 10

### Should be recommended Youtube Short Size
SIZE = (1080, 1920)
FPS = 30
# FOLDERS
VIDEO = 'video'
MUSIC = 'music'

### Is possible to send request to get 10 Text in one request. 
VID_TO_GENRATE = 1  # How many videos generate for each request
TEXT_TO_GENERATE = 1
PROMPT_TEMPLATE = f'Generate a convincing, witty, eloquent, unique and inspirational or motivational quote of 200-250 characters, never write it in quotations. The quote must be divided by punctuation signs like the comma, in short fragments of 5 or 6 words. Also, create a title, a short description and a list of 5 tags which represent the content of the quote. The quote, the title, the description and the list of tags must be separated by each other by "[m]", always in this way and order: "Quote [m] Title [m] Description [m] Tags" without indicating which is which. Never indicate which element is which. Dont use "#" to separate the tags, instead separate them by using commas. Never mention references, authors, or sources.' 

