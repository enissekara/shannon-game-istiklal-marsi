import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random
import matplotlib.pyplot as plt


url = "https://www.antoloji.com/istiklal-marsi-siiri/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


poem_div = soup.find("div", {"class": "pd-text"})
verses = poem_div.text.strip()


def clean_text(text):
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'c', 'Ğ': 'g', 'İ': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u'
    }
    for src, dest in replacements.items():
        text = text.replace(src, dest)
    return ''.join([c for c in text.lower() if c.isalpha() or c == ' '])

cleaned = clean_text(verses)


N = 3


model = defaultdict(lambda: defaultdict(int))
for i in range(len(cleaned) - N):
    context = cleaned[i:i+N]
    next_char = cleaned[i+N]
    model[context][next_char] += 1


def predict_next_char(context):
    if context in model:
        next_chars = model[context]
        return max(next_chars, key=next_chars.get)
    else:
        return random.choice('abcdefghijklmnopqrstuvwxyz ')


correct = 0
total = 0
correct_per_char = defaultdict(int)
total_per_char = defaultdict(int)

for i in range(len(cleaned) - N):
    context = cleaned[i:i+N]
    actual = cleaned[i+N]
    predicted = predict_next_char(context)
    
    total += 1
    total_per_char[actual] += 1
    if predicted == actual:
        correct += 1
        correct_per_char[actual] += 1


accuracy = correct / total * 100


print("Shannon Game – İstiklal Marşı Üzerinden Tahmin Testi")
print(f"Toplam harf sayısı       : {total}")
print(f"Doğru tahmin edilen harf : {correct}")
print(f"Başarı oranı             : {accuracy:.2f}%")


success = correct
failure = total - correct
labels = ['Doğru Tahmin', 'Yanlış Tahmin']
sizes = [success, failure]
colors = ['#4CAF50', '#F44336']
explode = (0.1, 0)

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, explode=explode,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Shannon Game – Tahmin Başarı Oranı")
plt.axis('equal')
plt.show()


chars = sorted(total_per_char.keys())
accuracies = [correct_per_char[c] / total_per_char[c] * 100 for c in chars]

plt.figure(figsize=(12, 5))
plt.bar(chars, accuracies, color="#2196F3")
plt.xlabel("Harf")
plt.ylabel("Başarı Oranı (%)")
plt.title("Her Harf İçin Tahmin Başarı Oranı")
plt.grid(axis='y')
plt.show()
