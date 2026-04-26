import os
import sys
import json

class Expert:
	def __init__(self, json_cfg, loc_file):
		# категорії виду { "тип" : [ID класів...] }
		self.categories = { "recycle": [], "conditional": [], "utilize": [] }
		self.guides_text = {}		# текст "гайду" для переробки
		with open(json_cfg, 'r') as cfg:
			expert_cfg = json.load(cfg)
			
			for k, v in expert_cfg.items():
				match v["type"].lower():
					case "recycle":
						self.categories["recycle"].append(int(k))
					case "conditional":
						self.categories["conditional"].append(int(k))
					case "utilize":
						self.categories["utilize"].append(int(k))
					case _:
						raise ValueError("unexpected category \'" + v["type"] + "\'")
				self.guides_text[int(k)] = ""
		
		with open(os.path.join("appdata", "localization", "expert", loc_file), 'r') as locale:
			loc_strings = json.load(locale)
			for k, v in loc_strings.items():
				if int(k) in self.guides_text:
					self.guides_text[int(k)] = v
				else:
					print(f"Unused expert guide localization {k}")
		
	def recommend(self, prediction):
		percentages = { "recycle": 0.0, "conditional": 0.0, "utilize": 0.0 }
		# рекомендації у вигляді { "категорія" : { клас : "гайд", ... }, ... }
		recommendations = { "recycle": {}, "conditional": {}, "utilize": {} }
		if prediction is None or not prediction:
			return recommendations
		
		total_objects = 0
		for _, cls, _ in prediction["predictions"]:
			if cls in self.categories["recycle"]:
				recommendations["recycle"][cls] = self.guides_text.get(cls, "")
				percentages["recycle"] += 1
			if cls in self.categories["conditional"]:
				recommendations["conditional"][cls] = self.guides_text.get(cls, "")
				percentages["conditional"] += 1
			if cls in self.categories["utilize"]:
				recommendations["utilize"][cls] = self.guides_text.get(cls, "")
				percentages["utilize"] += 1
			total_objects += 1
		
		percentages["recycle"] /= total_objects
		percentages["conditional"] /= total_objects
		percentages["utilize"] /= total_objects
		
		percentages["recycle"] *= 100.0
		percentages["conditional"] *= 100.0
		percentages["utilize"] *= 100.0
		
		return recommendations, percentages