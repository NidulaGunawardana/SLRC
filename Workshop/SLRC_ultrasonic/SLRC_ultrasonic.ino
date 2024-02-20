#define echoLeft 11
#define trigLeft 12
#define echoCent 7
#define trigCent 8
#define trigRight 3
#define echoRight 2


// Variable to store time taken to the pulse
// to reach receiver

// int distanceLeft;
// int distanceRight;
// int distanceCent;

int getLeftDistance() {
  long duration;
  int distance;
  digitalWrite(trigLeft, LOW);
  delayMicroseconds(2);  // wait for 2 ms to avoid
                         // collision in serial monitor

  digitalWrite(trigLeft, HIGH);  // turn on the Trigger to generate pulse
  delayMicroseconds(10);

  digitalWrite(trigLeft, LOW);  // Turn off the pulse trigger to stop

  duration = pulseIn(echoLeft, HIGH);
  distance = duration * 0.0344 / 2;  // Expression to calculate

  return distance;
}

int getCentDistance() {
  long duration;
  int distance;
  digitalWrite(trigCent, LOW);
  delayMicroseconds(2);  // wait for 2 ms to avoid
                         // collision in serial monitor

  digitalWrite(trigCent, HIGH);  // turn on the Trigger to generate pulse
  delayMicroseconds(10);

  digitalWrite(trigCent, LOW);  // Turn off the pulse trigger to stop

  duration = pulseIn(echoCent, HIGH);
  distance = duration * 0.0344 / 2;  // Expression to calculate

  return distance;
}

int getRightDistance() {
  long duration;
  int distance;
  digitalWrite(trigRight, LOW);
  delayMicroseconds(2);  // wait for 2 ms to avoid
                         // collision in serial monitor

  digitalWrite(trigRight, HIGH);  // turn on the Trigger to generate pulse
  delayMicroseconds(10);

  digitalWrite(trigRight, LOW);  // Turn off the pulse trigger to stop

  duration = pulseIn(echoRight, HIGH);
  distance = duration * 0.0344 / 2;  // Expression to calculate

  return distance;
}
void setup() {
  pinMode(trigLeft, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoLeft, INPUT);   // Sets the echoPin as an INPUT
  pinMode(trigCent, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoCent, INPUT);
  pinMode(trigRight, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoRight, INPUT);

  // Serial Communication is starting with 9600 of
  // baudrate speed
  Serial.begin(9600);

  // The text to be printed in serial monitor
  Serial.println(
    "Distance measurement using Arduino Uno.");
  delay(500);
}

void loop() {
  distanceLeft = getLeftDistance();
  distanceCent = getCentDistance();
  distanceRight = getRightDistance();

  Serial.println((String)distanceLeft + " " + (String)distanceCent + " " + (String)distanceRight);
}