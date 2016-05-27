/*
 * Silence Thresholder
 * For Chatty Coasters
 */

/* DECLARATIONS */

/* Discretize audio input to one sample every SAMPLE_WINDOW mS:
 * e.g. 50mS = 20Hz sample rate. */
const int sampleWindow = 50; 

/* After TIME_THRESH sampleWindows below VOL_THRESH, trigger event
 * 20Hz * 5S wait time = 100 */
int timeThresh = 100;
int timeThreshCount;

/* Record the average voltage over a window to be reported. */
float runningAverage = 0;
int windowSize = 100;
int currWindow = 0;

/* Thresholds for discretizing voltage to low, med, high.
 * WARNING: need to adjust based on audio input's hardware. */
const float lowThresh = 0.5f;
const float medThresh = 1.2f;
const float highThresh = 2.1f;

/* Function pointer to a function to activate after silence threshold
 * is achieved. */
void (*threshFunc)(float *) = NULL;

/* Function to run in setup to intially train the thresholder on how
 * chatty the converstaion is. Chattiness is a factor from 0.1 to
 * 1.0 representing quiet to loud. */
void trainPhrase(); // TODO
float chattiness; // TODO

/* Do not speak again for COOLDOWN milliseconds after speaking. */
int cooldown;
const int cooldownTime = 5000;

/* Threshold function declarations */
void blinkLed(float *);
void printThresh(float *);
void sendAudio(float *);

unsigned int sample;

/* Pin declarations */
int led = 13;

/* MAIN CODE */

void setup() {
    pinMode(led, OUTPUT);
    Serial.begin(9600);
    timeThreshCount = 0;
    // threshFunc = &printThresh;
    // threshFunc = &blinkLed;
    threshFunc = &sendAudio;

	// trainPhrase();
}


void loop() {
  unsigned long startMillis= millis();  // Start of sample window
	double volts = audioSample(startMillis);
//  Serial.print("Volts: ");
//	Serial.println(volts);
//  Serial.print("Window: ");
//  Serial.println(currWindow);

  if (++currWindow > windowSize)
  {
    runningAverage /= currWindow;
    threshFunc(&runningAverage);
    runningAverage = 0;
    currWindow = 0;
  }
  else
  {
    runningAverage += volts;
  }

}

double audioSample(unsigned long startMillis) {
    unsigned int peakToPeak = 0;   // peak-to-peak level
    unsigned int signalMax = 0;
    unsigned int signalMin = 1024;

    // collect data for 50 mS
    while (millis() - startMillis < sampleWindow)
    {
        sample = analogRead(0);
        if (sample < 1024)  // toss out spurious readings
        {
            if (sample > signalMax)
            {
                signalMax = sample;  // save just the max levels
            }
            else if (sample < signalMin)
            {
                signalMin = sample;  // save just the min levels
            }
        }
    }
    peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude
	return (peakToPeak * 3.3) /1024; // convert to volts
}

void trainPhrase() {
	// machine learning jazz maybe
}

void blinkLed(float *unused) {
    /* Intentionally block thread, do not listen during blocking */
    digitalWrite(led, HIGH);
    delay(2000);
    digitalWrite(led, LOW);
}

void printThresh(float *unused) {
    Serial.println("*********REACHED A THRESHOLD!**********");
}

void sendAudio(float *average) {
  //TODO: send average over serial, marshalling to be decided
  long normalizedAvg = *average * 100;
  normalizedAvg = constrain(normalizedAvg, 0, 100);
  normalizedAvg = map(normalizedAvg, 0, 100, 0, 1000);
  Serial.print("*********Boutta send some audio: ");
  Serial.print(normalizedAvg);
  Serial.print(", from unnormalized: ");
  Serial.print(*average);
  Serial.println("*********");
}

