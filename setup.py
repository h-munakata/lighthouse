from setuptools import setup, find_packages

setup(
    name='lighthouse',
    version='0.1',
    install_requires=['easydict', 'pandas', 'tqdm', 'pyyaml', 'scikit-learn', 'ffmpeg-python',
                      'ftfy', 'regex', 'tqdm', 'fvcore', 'gradio',
                      'clip@git+https://github.com/openai/CLIP.git'],
    packages=find_packages(),
)