import os

LOCALIZATION_EN = {
	#	recognition page
	"recog_btn_text" : "Detection",
	"gallery_btn_text" : "Gallery",
	"settings_btn_text" : "Settings",
	"find_objs_btn_text" : "Find objects",
	"classify_btn_text" : "Classify",
	"savefrags_btn_text" : "Save fragments...",
	"delfromgal_btn_text" : "Delete from gallery",
	"choose_image_text" : "Choose an image...",
	"statistics_tab" : "Statistics",
	"expert_tab" : "Recycling Expert",
	"statistics_text" : "Image dimensions [IWIDTH]x[IHEIGHT].\n[DCOUNT] objects detected.\n[AVGC]% average confidence.\nObject counts:\n[OBJC]",
	"expert_text" : "Can be recycled ([RECYCLED_PCNT]%):\n[RECYCLED]\nPossible recycling ([CONDITIONAL_PCNT]%):\n[CONDITIONAL]\nUtilize ([UTILIZED_PCNT]%):\n[UTILIZED]",
	#	settings page
	"yolo_path_text" : "YOLO path:",
	"expert_path_text" : "Expert system rules path:",
	"cnnc_path_text" : "Fragment classifier path:",
	"class_path_text" : "Classes file path:",
	"cls_colors_text" : "Class colors:",
	"lang_path_text" : "Localization file path:",
	"iou_threshold_text" : "IOU threshold:",
	"ui_scale_text" : "UI scale:",
	"font_size_text" : "Font size:",
	"imsize_text" : "CNN image size:",
	"clrgal_btn_text" : "Clear gallery",
	"resets_btn_text" : "Reset settings",
}

LOCALIZATION_UK = {
	#	recognition page
	"recog_btn_text" : "Розпізнавання",
	"gallery_btn_text" : "Галерея",
	"settings_btn_text" : "Налаштування",
	"find_objs_btn_text" : "Знайти об'єкти",
	"classify_btn_text" : "Класифікувати",
	"savefrags_btn_text" : "Зберегти фрагменти...",
	"delfromgal_btn_text" : "Видалити з галереї",
	"choose_image_text" : "Обрати фото...",
	"statistics_tab" : "Статистика",
	"expert_tab" : "ЕС вторинної переробки",
	"statistics_text" : "Зображення [IWIDTH]x[IHEIGHT].\nОб\'єктів знайдено: [DCOUNT].\nСередня впевненість: [AVGC]%.\nЗнайдені об\'єкти:\n[OBJC]",
	"expert_text" : "Придатні для переробки ([RECYCLED_PCNT]%):\n[RECYCLED]\nМожлива переробка ([CONDITIONAL_PCNT]%):\n[CONDITIONAL]\nНа утилізацію ([UTILIZED_PCNT]%):\n[UTILIZED]",
	#	settings page
	"yolo_path_text" : "Шлях до YOLO:",
	"expert_path_text" : "Шлях до правил експертної системи:",
	"cnnc_path_text" : "Шлях до класифікатора фрагментів:",
	"class_path_text" : "Шлях до файла з класами:",
	"cls_colors_text" : "Кольори класів:",
	"lang_path_text" : "Шлях до файла локалізації:",
	"iou_threshold_text" : "Поріг IOU:",
	"ui_scale_text" : "Масштаб інтерфейсу:",
	"font_size_text" : "Розмір тексту:",
	"imsize_text" : "Розмір зображення для CNN:",
	"clrgal_btn_text" : "Очистити галерею",
	"resets_btn_text" : "Скинути налаштування",
}

USER_SETTINGS = {
	"QT_SCALE" : 1.0, 
	"QT_BHEIGHT" : 40, 
	"QT_FONT_SIZE" : 16, 
	"LOC_PATH" : os.path.join("appdata", "localization", "en.json"), 
	"YOLO_PATH" : "",
	"CNNC_PATH" : "",
	"CLASS_PATH" : "",
	"EXPERT_PATH" : "",
	"IOU_THRESHOLD" : 0.75,
	"IMAGE_SIZE" : [224,224],
	"GALLERY" : [],
	"CLASS_COLORS" : {},
}

STATISTICS_FMTK = {
	"IWIDTH" : None,		# image width, int or None
	"IHEIGHT" : None,		# image height, int or None
	"DCOUNT" : None,		# detections count, int or None
	"AVGC" : None			# average confidence, float or None
}

EXPERT_FMTK = {
	"RECYCLED" : None,		# recycled objects, str or None
	"UTILIZED" : None,		# utilized objects, str or None
	"CONDITIONAL" : None,	# conditionally recycled, str or None
	"RECYCLED_PCNT" : None,	# recycled percentage, float or None
	"UTILIZED_PCNT" : None,	# conditionally recycled percentage, float or None
	"CONDITIONAL_PCNT" : None,	# utilized percentage, float or None
}

GALLERY_OBJECT = {
	"classified" : False,
	"preview" : None,			# image preview (QPixbuf)
	"image" : None,				# image data
	"proc_image" : None,		# post-processed image data
	"predictions" : None		# found(and probably classified) objects
}