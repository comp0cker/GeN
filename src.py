import sound
import time
import mingus.core.notes
import mingus.core.chords
import mingus.core.progressions

class Note:
	def __init__(self, pitch_in, duration_in):
		self.pitch = pitch_in
		self.duration = duration_in

class Player:
	def __init__(self):
		self.play = Play()
		self.song_arr = []
		
		self.bpm = 120
		self.key = 'C'
	
	def chord_name(self, phrase, delim):
		return phrase.split(delim)[0]
	
	def end_note(self, char):
		return char == "#" or char == "b" or char.isdigit()
		
	def queue_notes(self):				
		i = input('input: ')
		input_arr = i.split(' ')
		rhythm_tag = ''

		for phrase in input_arr:
			phrase_arr = []
			phrase_queue = ''
			duration = 4
			
			if '(' in phrase:
				rhythm_tag = '-' + phrase.split('(')[0]
				phrase = phrase.split('(')[1]
				
			phrase += rhythm_tag
				
			if ')' in phrase:
				rhythm_tag = ''
				phrase = phrase.split(')')[0] + phrase.split(')')[1]
			
			# If the note inputted has a duration specified
			if '-' in phrase:
				 duration = float(phrase.split('-')[1])
				 phrase = phrase.split('-')[0]
			
			# If the phrase is setting the tempo
			if 'd=' in phrase:
				self.bpm = float(phrase.split('d=')[1])
				
			# If the phrase is setting the key
			elif 'key=' in phrase:
				self.key = phrase.split('key=')[1]
				
			# If the phrase is a diatonic chord
			elif 'i' in phrase.lower() or 'v' in phrase.lower():
				if phrase.islower() and len(phrase) <= 3:
					phrase += 'm'
				elif phrase.isupper():
					phrase += 'M'
				
				self.song_arr.append(Note(mingus.core.progressions.to_chords([phrase], self.key)[0], duration))
				# print(mingus.core.progressions.to_chords([phrase], self.key))
			
			# If an absolute chord is recognized
			elif any(char.isdigit() for char in phrase) or 'm' in phrase.lower():
				self.song_arr.append(Note(mingus.core.chords.from_shorthand(phrase), duration))
			
			# If the phrase is just a bunch of letters
			else:
				for char in phrase:
					if len(phrase_queue) > 0 and self.end_note(char) == False:
							phrase_arr.append(phrase_queue)
							phrase_queue = ""
					phrase_queue += char
				
				phrase_arr.append(phrase_queue)
				self.song_arr.append(Note(phrase_arr, duration))
			
	def play_song(self):
		for phrase in self.song_arr:
			self.play.chord(phrase.pitch)
			time.sleep(60 * 4 / (phrase.duration * self.bpm))

class Play:
	def __init__(self):
		self.notes = mingus.core.notes
	def note(self, note):
		if 'b' in note:
			note = self.notes.int_to_note(self.notes.note_to_int(note))

		# To get it to work with built in sound lib			
		if note[-1].isdigit() == False:
			note += '3'

		if '#' in note:
			note = note.split('#')[0] + note.split('#')[1] + '#'		
		sound.play_effect('piano:' + note)
		
	def chord(self, notes):
		
		# Why does this have to exist... Thanks mingus
		if notes[-1] in ['3', '']:
			notes.pop()
			
		label = mingus.core.chords.determine(notes)
		if len(label) == 0:
			print(notes)
		else:
			print(label[0])
		for note in notes:
			self.note(note)

player = Player()
player.queue_notes()
player.play_song()
