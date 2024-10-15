#include "control.h"

void emergency_shutdown()
{
    digitalWrite(PIN_ARDUINO_PWR, LOW);
}

void initHardware()
{
    // Configure the ultrasonic sensors
    pinMode(PIN_US_WATER_TRIGGER, OUTPUT);
    pinMode(PIN_US_WATER_ECHO, INPUT);

    pinMode(PIN_US_FERTILIZER_TRIGGER, OUTPUT);
    pinMode(PIN_US_FERTILIZER_ECHO, INPUT);

    pinMode(PIN_US_ACID_TRIGGER, OUTPUT);
    pinMode(PIN_US_ACID_ECHO, INPUT);

    // Configure the PH sensor
    pinMode(PIN_PH_PO, ANALOG);
    analogReadResolution(12); // Set ADC resolution to 12 bits

    Serial.println("initialized Hardware");
}

float readUltraSonic(int trigger_pin, int echo_pin)
{
    Serial.println("reading distance from us sensor");
    digitalWrite(trigger_pin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigger_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger_pin, LOW);

    // Measure the echo pulse duration
    long duration = pulseIn(echo_pin, HIGH);

    // Calculate the distance (in cm)
    float distance = duration * 0.034 / 2;
    Serial.printf("distance is %d cm\n", distance);
    return distance;
}

void bubbleSort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                // Tausche arr[j] und arr[j+1]
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

float findMedian(int arr[], int n)
{
    if (n % 2 == 0)
    {
        // Wenn n gerade ist, den Durchschnitt der beiden mittleren Werte berechnen
        return (arr[n / 2 - 1] + arr[n / 2]) / 2.0;
    }
    else
    {
        // Wenn n ungerade ist, den mittleren Wert zurückgeben
        return arr[n / 2];
    }
}

float analogToPH(int analogVal){
    float calibration_value = 0.15;

    float voltage = analogVal * (3.0 / 4095.0) + calibration_value;
    // Berechnung PH
    //   pH = 7 + (voltage-1.5)*(4-7)/(1.7-1.5);

    return ((0.07 * 7 - voltage + 1.5) / 0.07) ;
}

float read_PH()
{
    float pH, diffPH, testPH_arr[10], diffPH_avg;
    int buffer_arr[9];

    while (1)
    {
        for (int i = 0; i < 10; i++)
        {
            testPH_arr[i] = analogToPH(analogRead(PIN_PH_PO));
            delay(1000);
        }
        for (int i = 0; i < 9; i++)
        {
            diffPH_avg += testPH_arr[i + 1] - testPH_arr[i];
        }
        
        diffPH_avg /= 9;
        Serial.printf("average difference: %f\n", diffPH_avg);


        if(diffPH_avg < 0.2)
            break;

        delay(1000 * 60);
    }

    for (int i = 0; i < 9; i++)
    {
        buffer_arr[i] = analogRead(PIN_PH_PO);
        delay(1000);
    }

    bubbleSort(buffer_arr, 9);

    float median = findMedian(buffer_arr, 9);

    pH = analogToPH(median);

    Serial.printf("ph is %f\n", pH);

    return pH;
}

bool addWater(int ml)
{
    Serial.printf("adding %dml of water\n", ml);
    Serial.println(CMD_PUMP_WATER_ON);
    /* Serial.flush();
    delay(1000);
    if (arduinoResponse() != ACK_PUMP_WATER_ON){
        Serial.println(CMD_PUMP_WATER_OFF);
        return false;
    } */
    delay(ml * C_TIME_VOL);
    Serial.println(CMD_PUMP_WATER_OFF);
    /* if (arduinoResponse() != ACK_PUMP_WATER_OFF){
        emergency_shutdown();
        return false;
    } */
    return true;
}

bool addFertilizer(int ml)
{
    Serial.printf("adding %dml of fertilizer\n", ml);
    Serial.println(CMD_PUMP_FERTILIZER_ON);
    /* Serial.flush();
    delay(1000);
    if(arduinoResponse() != ACK_PUMP_FERTILIZER_ON){
        Serial.println(CMD_PUMP_FERTILIZER_ON);
        return false;
    } */
    delay(ml * C_TIME_VOL);
    Serial.println(CMD_PUMP_FERTILIZER_OFF);
    /* if(arduinoResponse() != ACK_PUMP_FERTILIZER_OFF){
        emergency_shutdown();
        return false;
    } */
    return true;
}

bool correctPH(float ph)
{
    Serial.println("reading PH from Sensor");
    // int ml = ph * C_PH_VOL;
    int ml = 20;
    float curr_ph;
    for (int i = 0; i <= 5; i++)
    {
        delay(1000 * 60 * 10);
        curr_ph = read_PH();
        if (curr_ph <= ph)
            break;
        Serial.println(CMD_PUMP_ACID_ON);
        /* Serial.flush();
        delay(1000);
        if(arduinoResponse() != ACK_PUMP_ACID_ON){
            Serial.println(CMD_PUMP_ACID_OFF);
            return false;
        } */
        delay(ml * C_TIME_VOL);
        Serial.println(CMD_PUMP_ACID_OFF);
        /* if(arduinoResponse() != ACK_PUMP_ACID_OFF){
            emergency_shutdown();
            return false;
        } */
    }
    return true;
}

bool waterPlant(int pumpID)
{
    Serial.printf("pumping water mixture into pot %d\n", pumpID);
    Serial.printf("CMD_PUMP%d_ON\n", pumpID);
    /* Serial.flush();
    delay(1000);
    if(arduinoResponse() != CMD_PUMP_POT_ON(pumpID)){
        Serial.println(CMD_PUMP_POT_OFF(pumpID));
        return false;
    } */
    delay(200 * C_TIME_VOL);
    // Serial.println(CMD_PUMP_POT_OFF(pumpID));                    //CMD_PUMPx_LOW -> 0x0
    Serial.printf("CMD_PUMP%d_OFF\n", pumpID);

    /* if(arduinoResponse() != CMD_PUMP_POT_OFF(pumpID)){
        emergency_shutdown();
        return false;
    } */
    return true;
}

String arduinoResponse()
{
    String response;

    while (Serial.available() > 0)
    {
        char inChar = Serial.read();

        if (inChar != '\n')
        {
            response += inChar;
        }
        else
        {
            response.trim();
        }
    }
    Serial.println(response);
    return response;
}