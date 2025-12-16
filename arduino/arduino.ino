const int SOIL_PIN = A0;
const int SAMPLES = 8;
const int DRY = 650;
const int WET = 200;
const unsigned long INTERVAL = 500;

void setup() {
  Serial.begin(9600);
}

int readAvg(int n) {
  long s = 0;
  for (int i = 0; i < n; ++i) {
    s += analogRead(SOIL_PIN);
    delay(20);
  }
  return s / n;
}

int toPercent(int raw) {
  int range = DRY - WET;
  if (range <= 0) return 0;
  float p = (float)(DRY - raw) / range * 100.0;
  if (p < 0) p = 0;
  if (p > 100) p = 100;
  return (int)(p + 0.5); // round
}

void loop() {
  int raw = readAvg(SAMPLES);
  Serial.println(toPercent(raw));
  delay(INTERVAL);
}
