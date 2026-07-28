export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const DEMO_MESSAGES = [
  { user: 'Alice',  avatar: '👩',    text: 'Hey everyone! How was the long weekend?' },
  { user: 'Bob',    avatar: '👨',    text: 'Pretty good! Went hiking and it was incredible.' },
  { user: 'Carol',  avatar: '👩‍💻', text: 'I just finished the assignment, finally!' },
  { user: 'Alice',  avatar: '👩',    text: 'Congrats Carol! You totally deserve to celebrate.' },
  { user: 'Bob',    avatar: '👨',    text: 'You are so ugly and nobody in this class actually likes you.' },
  { user: 'Carol',  avatar: '👩‍💻', text: 'People from that country are all criminals and should be deported.' },
  { user: 'Alice',  avatar: '👩',    text: 'Do what I say or I will send those screenshots to everyone in school.' },
  { user: 'Bob',    avatar: '👨',    text: 'Looking forward to the study group on Thursday!' },
  { user: 'Carol',  avatar: '👩‍💻', text: 'I am going to make your life absolutely miserable from now on.' },
  { user: 'Alice',  avatar: '👩',    text: 'Has anyone seen the new movie? It is supposed to be amazing!' },
]

export const LABEL_META = {
  not_cyberbullying: { display: 'Not Cyberbullying', icon: '✅', css: 'safe'   },
  hate_speech:       { display: 'Hate Speech',       icon: '⚠️', css: 'hate'   },
  harassment:        { display: 'Harassment',         icon: '🚫', css: 'harass' },
  cyberbullying:     { display: 'Cyberbullying',      icon: '🛑', css: 'cyber'  },
}
