export const LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'zu', name: 'isiZulu', nativeName: 'isiZulu' },
  { code: 'af', name: 'Afrikaans', nativeName: 'Afrikaans' },
  { code: 'es', name: 'Spanish', nativeName: 'Español' },
  { code: 'fr', name: 'French', nativeName: 'Français' }
];

export const MEDICAL_TEST_RANGES = {
  'blood_pressure': { min: 90, max: 120, unit: 'mmHg' },
  'cholesterol': { min: 0, max: 200, unit: 'mg/dL' },
  'glucose': { min: 70, max: 140, unit: 'mg/dL' },
  'hemoglobin': { min: 13.5, max: 17.5, unit: 'g/dL' },
  'platelets': { min: 150, max: 450, unit: '×10³/μL' }
};

export const MEDICAL_TERMS = {
  'Hypertension': 'High blood pressure',
  'Hyperlipidemia': 'High cholesterol levels',
  'Diabetes Mellitus': 'Condition with high blood sugar',
  'Anemia': 'Low red blood cell count',
  'Leukocytosis': 'High white blood cell count',
  'Thrombocytopenia': 'Low platelet count',
  'Hyperglycemia': 'High blood sugar',
  'Hypoglycemia': 'Low blood sugar'
};

export const SA_MEDICAL_PHRASES = {
  isiZulu: {
    welcome: 'Sawubona! Sizokusiza ukuqonda irekhodi lakho lezempilo.',
    thank_you: 'Ngiyabonga ngokufunda ucwaningo lwakho.',
    consult_doctor: 'Xhumana nodokotela wakho ukuze uthole iseluleko esiphelele.',
    emergency: 'Uma unezimo eziphuthumayo, shayela u-112 noma uye esibhedlela.'
  },
  Afrikaans: {
    welcome: 'Welkom! Ons sal jou help om jou mediese verslag te verstaan.',
    thank_you: 'Dankie dat jy jou verslag gelees het.',
    consult_doctor: 'Raadpleeg jou dokter vir volledige advies.',
    emergency: 'In geval van nood, skakel 112 of gaan na die hospitaal.'
  }
};