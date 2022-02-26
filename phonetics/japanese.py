import cutlet
katsu = cutlet.Cutlet()

# katsu.romaji("カツカレーは美味しい")
# => 'Cutlet curry wa oishii'

# you can print a slug suitable for urls
# katsu.slug("カツカレーは美味しい")
# => 'cutlet-curry-wa-oishii'

# You can disable using foreign spelling too
katsu.use_foreign_spelling = False
# katsu.romaji("カツカレーは美味しい")
# => 'Katsu karee wa oishii'

# kunreisiki, nihonsiki work too
# katu = cutlet.Cutlet('kunrei')
# katu.romaji("富士山")
# => 'Huzi yama'

# # comparison
# nkatu = cutlet.Cutlet('nihon')

# sent = "彼女は王への手紙を読み上げた。"
# katsu.romaji(sent)
# # => 'Kanojo wa ou e no tegami wo yomiageta.'
# katu.romaji(sent)
# # => 'Kanozyo wa ou e no tegami o yomiageta.'
# nkatu.romaji(sent)
# # => 'Kanozyo ha ou he no tegami wo yomiageta.'

def add_kana(lines):
	for i in lines:
		j = katsu.romaji("カツカレーは美味しい")