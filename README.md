# ABOUT
This repository contains software implementation of a neural network classification method for construction waste for the needs of the circular economy ("Метод нейромережевої класифікації відходів будівництва для потреб циркулярної економіки"). Below are the instructions for installation, configuration and using the software.

# Dependencies
Before using any of these applications, please install required dependencies from `requirements.txt` file using pip: 

`pip install -r requirements.txt`

# Pixelano (pixelano.py)
Pixel Annotator (or simply "Pixelano") is a simple utility which allows user to graphically annotate images and produces PASCAL VOC-annotated dataset from input data.
It has simple CLI:
```
Usage: pixelano.py <parameters>
	Possible parameters:
		-clm <path> = class to color map file path
			file needs to be filled with lines in following format:
				'<CLASS_NAME><TABULATION><LOWER RGB VALUE><TABULATION><UPPER RGB VALUE>', e.g. 'MyClass	220;0;0	255;0;0'
		-f <path> = specify path to single image file
			-f path/to/my/img.jpg
		-d <path> = specify path to directory with images
			-d path/to/my/images
		-o <path> = specify dataset output path
```

# QT App(qtapp.py)
Is a GUI application with a fair amount of configurations (both for classification tasks and cosmetic settings), which allows to use trained YOLO and ResNet50 or other neural network models to find and classify objects on images. 

Run using:

`python qtapp.py`

# QT App classes file
QT App needs a list of classes to perform classifications, this can be defined in a JSON file using a pattern as in the example below. Unless you are using hand-crafted dataset, you can just use `classes.json` file from `reprod_data` to load classes in QT App settings and skip this section.
```json
{
  "0" : {
    "uk" : "Мій клас"
    "en" : "My class"
    "default" : "MyClass"
  }
  "1" : {
    "uk" : "Мій інший клас"
    "en" : "My other class"
    "default" : "MyOtherClass"
  }
}
```
Each entry is a (`id`, `dict`) pair, where `id` is a numerical string, representing class label and `dict` contains localization data, used to describe class label when post-processing a classified image, contains (`lang`, `text`) pairs, where `lang` is a localization identifier and `text` is a string to be displayed with `lang` localization on. 
"default" localization name is used, when QT App's turned localization name was not found in `dict`.

# QT App Recycling Expert
QT App supports the enabling of "Recycling Expert", an Expert System to give recommendations on how to recycle detected objects on an image. This ES is defined in a separate JSON file, by default the application doesn't automatically define it, as it has no knowledge of user's dataset, and even if it does, it has no idea on what classes the user expects to be recycled or utilized.

To define an expert system for recycling, one needs to create a new JSON file and fill it in similar fashion to this example:
```json
{
  "0" : {
   "type" : "recycle"
  }
  "1" : {
   "type" : "conditional"
  }
  "2" : {
    "type" : "utilize"
  }
}
```

Each entry is a (`id`, `dict`) pair, where `id` is a numerical string, representing class label and `dict` contains classification data for expert system (for now it only needs `type` of group, but there can be additional metadata in the future). Recycling Expert divides objects into three groups: `recycle`, `conditional` and `utilize`.
The guide on allocating groups is the following:
- One should put classes that can always be recycled to `recycle` group
- If a class can only be recycled when certain conditions are met, then it must be put into `conditional` group
- Classes of objects that can not be recycled are put into `utilize` group
After creating an expert configuration file, one also needs to provide localizations for the app, which should be put into `appdata/localization/expert`.

Localization is created just like it is done for the rest of the application, localizer should name the file with locale name(e.g. `en.json` or `uk.json`) and fill it as in this example:
```json
{
	"0": "This class can be recycled by following these steps: ...",
	"1": "This class can only be recycled if these conditions are met: ...",
	"2": "This class must be utilized ..."
}
```

With this information, QT application will have all the sufficient information to start recommending recycling strategies for found objects.

# QT App Fragment Classifiers
Application uses a simple, home-grown MLC(Model Loader Config) language to specify all necessary data for it to load classifiers.

To provide a fragment classifier(or a cascade of such) to QT App one needs to create a text file with `.mlc` extension and fill it with data as in examples below. 

QT App has built-in capabilities to load ResNet50 binary classifier ensembles("cascades").

To load them, one writes following in his new `.mlc` file:
```
type	cascade
section	classes
0	rn50_tarbrick/model.keras
1	rn50_tarconcr/model.keras
2	rn50_tarfoam/model.keras
3	rn50_targw/model.keras
4	rn50_targb/model.keras
5	rn50_tarpipes/model.keras
6	rn50_tarplast/model.keras
7	rn50_tarstone/model.keras
8	rn50_tartile/model.keras
9	rn50_tarwood/model.keras
endsection
```

First, `type cascade` signalizes, that this model config will use built-in model loading capabilities, then, `section classes` defines a map of class label(first column) to model path(second column), `endsection` finishes the section definition, all values and identifiers are separated by tabulation, this is necessary to correctly parse all definitions.
If one wants to use custom trained model with this application, they should follow example below:
```
type	custom
section	loader
# here goes Python code, which loads your model
# you can import libraries to aid you with it, e.g.:
from keras.models import load_model
model = load_model("path/to/mymodel.keras")
# you can do other setup operations with your model here, if it is necessary
# naming variable "model" is mandatory, as application expects this to fetch loaded model 
endsection
section	preproc
# here goes Python code, which defines preprocessor function for model's input image
# you must return variable or function named "preproc" here, e.g.:
def preproc(img, img_size):
  # preprocessing of img...
endsection
# here goes Python code, which defines predict functionality for custom model
# you must define a "predict" function, with following signature:
def predict(model, preproc, data, image_size):
  # your prediction logic goes here...
endsection
section	classes
# here goes mapping of model predicted labels to class ids used by QT App
# e.g.:
# 0	0 <-- predicted label 0 corresponds to class 0 defined in classes file(see "QT App classes file")
# you can leave this section empty, if there's no need to do re-mapping between your model predictions and application classes map
endsection

```

Summary from example above: user(or a person, responsible for training the model) defines MLC file with `type	custom` header, then proceeds by defining `loader`, `preproc`, `predict` and `classes` sections, first three contain Python code, `loader` needs to return `model` variable, `preproc` needs to return `preproc` function or variable(pointer to function), `predict` which needs to return `predict` function, last one is a map of labels to class names used by application in post-processing.

# Creating localization for QT App
To create a new localization for QT App one needs to navigate to "appdata/localization"(if appdata doesn't exist, just run the qtapp.py once and it will be automatically created) and create new JSON file there, file's name without extension will be used to identify new localization.

In JSON file localizer needs to specify label names to set localized text for:
```json
{
  "recog_btn_text" : "Detection button text"
}
```

Label names list used in app is as follows:
```
    recog_btn_text - Detection tab button,
    gallery_btn_text - Gallery tab button,
    settings_btn_text - Settings tab button,
    find_objs_btn_text - Button to trigger object search (Detection tab),
    classify_btn_text - Button to trigger found objects classification (Detection tab),
    savefrags_btn_text - Button to save found objects' image fragments (Detection & Gallery tab),
    delfromgal_btn_text - Button to delete detection result from gallery (Detection & Gallery tab),
    choose_image_text - Placeholder text for image displayer widget in detection tab (Detection tab),
    statistics_text - Statistics text for detection result (Detection & Gallery tab),
    yolo_path_text - YOLO path label (Settings tab),
    cnnc_path_text - CNN cascade path label (Settings tab),
    class_path_text - Classes file path label (Settings tab),
    cls_colors_text - Class colors label (Settings tab),
    lang_path_text - Localization file path label (Settings tab),
    iou_threshold_text - IoU threshold label (Settings tab),
    ui_scale_text - UI scale label (Settings tab),
    font_size_text - Font size label (Settings tab),
    imsize_text - CNN image size label (Settings tab),
    clrgal_btn_text - Button to clear gallery (Settings tab),
    resets_btn_text - Button to reset settings (Settings tab)
```

If description above seems confusing or hard to follow, you can run QT App with empty localization file and see, which label names appear where and have better understanding, what text needs to be there.

statistics_text string accepts following format specifiers:

```
  IWIDTH - image width
  IHEIGHT - image height
  DCOUNT - object detections count
  AVGC - average confidence
  OBJC - detected objects with counts
```

expert_text string accept following format specifiers:

```
	RECYCLED - expert guide to recycle objects, for which it is possible
	CONDITIONAL - expert guide to recycle objects, which can either be recycled or utilized, depending on their state
	UTILIZED - expert guide to utilize objects
	RECYCLED_PCNT - percentage of objects for recycling
	CONDITIONAL_PCNT - percentage of objects for possible recycling
	UTILIZED_PCNT - percentage of objects for utilization 
```

Format specifiers are written in brackets: 
```json
{
  "statistics_text" : "[IWIDTH]x[IHEIGHT] image, [DCOUNT] objects found\nObjects on image:\n[OBJC]"
}
```

If format specifier value is unknown (e.g. AVGC is known only after classification, not just object detection), it will be expanded into "---".
