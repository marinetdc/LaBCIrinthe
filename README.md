# LaBCIrinthe


LaBCIrithe is a 2D game implemented in pygame and Android application. It takes two kinds of information: orientation of the smartphone used to play the Android application and physiological signals. These information are used to render the scene correspondingly. The orientation of the smartphone determines the direction the avatar moves while the electrodermal signals change the physiological signals control the visibility and the colours of the environment.


## File organisation

- the directory `main` contains Android application. The application itself is organised in a typical Android project format, i.e. `src` file which contains two Java scripts `MainActivity.java` which serves as the main and `DisplayView.java` which draws the arrow in the direction of the gravitational pull and `res` which ontains resources such as `layout`
- The main game is written is python and is contained in the directory `src`
