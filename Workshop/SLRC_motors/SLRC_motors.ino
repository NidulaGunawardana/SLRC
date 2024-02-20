#define echoLeft 11
#define trigLeft 12
#define echoCent 7
#define trigCent 8
#define trigRight 3
#define echoRight 2

int distanceLeft;
int distanceRight;
int distanceCent;


double motorSpeedA;
double motorSpeedB;
double baseSpeed = 150;
double turnSpeed = 200;
double offset = 50;



int in1 = 5;
int in2 = 6;

int in3 = 9;
int in4 = 10;

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

void runMotors() {
  double MSpeedA = baseSpeed + offset;
  double MSpeedB = baseSpeed - offset;
  analogWrite(in1, MSpeedA);
  analogWrite(in2, 0);
  analogWrite(in3, MSpeedB);
  analogWrite(in4, 0);


  delay(50);  //offset has been added to balance motor speeds
}

void goForward() {
  runMotors();
}

void turnLeft(int turnDelay) {
  double MSpeedA = turnSpeed + offset;  //
  double MSpeedB = turnSpeed - offset;
  analogWrite(in1, 0);
  analogWrite(in2, MSpeedA);
  analogWrite(in3, MSpeedB);
  analogWrite(in4, 0);
  delay(turnDelay);
  analogWrite(in1, 0);
  analogWrite(in2, 0);
  analogWrite(in3, 0);
  analogWrite(in4, 0);
}

void turnRight(int turnDelay) {
  double MSpeedA = turnSpeed + offset;  //
  double MSpeedB = turnSpeed - offset;
  analogWrite(in1, MSpeedA);
  analogWrite(in2, 0);
  analogWrite(in3, 0);
  analogWrite(in4, MSpeedB);
  delay(turnDelay);
  analogWrite(in1, 0);
  analogWrite(in2, 0);
  analogWrite(in3, 0);
  analogWrite(in4, 0);
}

void stop() {

  analogWrite(in1, 0);
  analogWrite(in2, 0);
  analogWrite(in3, 0);
  analogWrite(in4, 0);
  delay(100);
}



void setup() {
  pinMode(trigLeft, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoLeft, INPUT);   // Sets the echoPin as an INPUT
  pinMode(trigCent, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoCent, INPUT);
  pinMode(trigRight, OUTPUT);  // Sets the trigPin as an OUTPUT
  pinMode(echoRight, INPUT);


  // put your setup code here, to run once:
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  Serial.begin(9600);

  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}



void loop() {
  // put your main code here, to run repeatedly:
  // turnLeft(500);
  distanceLeft = getLeftDistance();
  distanceCent = getCentDistance();
  distanceRight = getRightDistance();

  Serial.println(distanceCent);
  if (distanceCent < 10) {
    if (distanceLeft > 10) {
      turnLeft(500);
      Serial.println("inthe loop");
    } else if (distanceRight > 10) {
      turnRight(500);
    }
  } else {
    goForward();
  }
}
