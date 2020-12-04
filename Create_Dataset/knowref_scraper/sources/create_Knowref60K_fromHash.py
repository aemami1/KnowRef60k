import json
import hashlib

#Create Test-Set
print("Creating Test set...")
with open("knowref_scraper/sources/final_data/KnowRef-60K_test.json","a",encoding='utf-8') as f1:
	with open("knowref_scraper/sources/hashed_dataset/KnowRef-60K_test_hashed.json","r",encoding='utf-8') as f2:
		with open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json","r",encoding='utf-8') as f3:
			data={}
			data2=json.load(f2)
			data3=open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json").readlines()
			counter=1
			for lineGold in data2:
				for line3 in data3:
					lineCompare=json.loads(line3)
					if lineGold['original_sentence_hashed']==hashlib.sha224(lineCompare['original_sentence'][0].encode('utf-8')).hexdigest():
						data['original_sentence']=lineCompare['original_sentence'][0]
						data['swapped_sentence']=lineCompare['original_sentence'][0].replace(lineCompare['candidate0'][0],lineGold['candidate0']).replace(lineCompare['candidate1'][0],lineGold['candidate1'])
						data['candidate0']=lineGold['candidate0']
						data['candidate1']=lineGold['candidate1']
						data['correct_candidate']=lineGold['correct_candidate']
						data['annotation_strength']=lineGold['annotation_strength']
						

						f1.write(json.dumps(data)+'\n')

#Create Val
print("Creating Val set...")
with open("knowref_scraper/sources/final_data/KnowRef-60K_val.json","a",encoding='utf-8') as f1:
	with open("knowref_scraper/sources/hashed_dataset/KnowRef-60K_val_hashed.json","r",encoding='utf-8') as f2:
		with open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json","r",encoding='utf-8') as f3:
			data={}
			data2=json.load(f2)
			data3=open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json").readlines()
			counter=1
			for lineGold in data2:
				for line3 in data3:
					lineCompare=json.loads(line3)
					if lineGold['original_sentence_hashed']==hashlib.sha224(lineCompare['original_sentence'][0].encode('utf-8')).hexdigest():
						data['original_sentence']=lineCompare['original_sentence'][0]
						data['swapped_sentence']=lineCompare['original_sentence'][0].replace(lineCompare['candidate0'][0],lineGold['candidate0']).replace(lineCompare['candidate1'][0],lineGold['candidate1'])
						data['candidate0']=lineGold['candidate0']
						data['candidate1']=lineGold['candidate1']
						data['correct_candidate']=lineGold['correct_candidate']
						data['annotation_strength']=lineGold['annotation_strength']
						

						f1.write(json.dumps(data)+'\n')

#Create Val
print("Creating Dev set...")
with open("knowref_scraper/sources/final_data/KnowRef-60K_dev.json","a",encoding='utf-8') as f1:
	with open("knowref_scraper/sources/hashed_dataset/KnowRef-60K_dev_hashed.json","r",encoding='utf-8') as f2:
		with open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json","r",encoding='utf-8') as f3:
			data={}
			data2=json.load(f2)
			data3=open("knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json").readlines()
			counter=1
			for lineGold in data2:
				for line3 in data3:
					lineCompare=json.loads(line3)
					if lineGold['original_sentence_hashed']==hashlib.sha224(lineCompare['original_sentence'][0].encode('utf-8')).hexdigest():
						data['original_sentence']=lineCompare['original_sentence'][0]
						data['swapped_sentence']=lineCompare['original_sentence'][0].replace(lineCompare['candidate0'][0],lineGold['candidate0']).replace(lineCompare['candidate1'][0],lineGold['candidate1'])
						data['candidate0']=lineGold['candidate0']
						data['candidate1']=lineGold['candidate1']
						data['correct_candidate']=lineGold['correct_candidate']
						data['annotation_strength']=lineGold['annotation_strength']
						

						f1.write(json.dumps(data)+'\n')

