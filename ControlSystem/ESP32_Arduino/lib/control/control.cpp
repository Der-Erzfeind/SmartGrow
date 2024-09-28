#include "control.h"

void emergency_shutdown(){
    digitalWrite(PIN_ARDUINO_PWR, LOW);
}

void initHardware() {
    // Configure the ultrasonic sensors
    pinMode(PIN_US1_TRIGGER, OUTPUT);
    pinMode(PIN_US1_ECHO, INPUT);
    
    pinMode(PIN_US2_TRIGGER, OUTPUT);
    pinMode(PIN_US2_ECHO, INPUT);
    
    pinMode(PIN_US3_TRIGGER, OUTPUT);
    pinMode(PIN_US3_ECHO, INPUT);

    // Configure the PH sensor
    pinMode(PIN_PH_PO, ANALOG);

    Serial.println("initialized Hardware");
}

float readUltraSonic(int trigger_pin, int echo_pin) {
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

bool addWater(int ml){
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

bool addFertilizer(int ml){
    Serial.printf("adding %dml of fertilizer\n", ml);
    Serial.println(CMD_PUMP_FERTILIZER_ON);
    /* Serial.flush();
    delay(1000);
    if(arduinoResponse() != ACK_PUMP_FERTILIZER_ON){
        Serial.println(CMD_PUMP_FERTILIZER_ON);
        return false;
    } */
    delay(ml*C_TIME_VOL);
    Serial.println(CMD_PUMP_FERTILIZER_OFF);
    /* if(arduinoResponse() != ACK_PUMP_FERTILIZER_OFF){
        emergency_shutdown();
        return false;
    } */
    return true;
}

bool correctPH(float ph){
    Serial.println("reading PH from Sensor");
    int ml = ph * C_PH_VOL;
    float curr_ph;
    for(int i=0; i<=5; i++){
        curr_ph = read_PH();
        if(curr_ph <= ph) 
            break;
        Serial.println(CMD_PUMP_ACID_ON);
        /* Serial.flush();
        delay(1000);
        if(arduinoResponse() != ACK_PUMP_ACID_ON){
            Serial.println(CMD_PUMP_ACID_OFF);
            return false;
        } */
        delay(ml*C_TIME_VOL);
        Serial.println(CMD_PUMP_ACID_OFF);
        /* if(arduinoResponse() != ACK_PUMP_ACID_OFF){
            emergency_shutdown();
            return false;
        } */
        delay(1000 * 300);
    }
    return true;
}

bool waterPlant(int pumpID){
    Serial.printf("pumping water mixture into pot %d\n", pumpID);
    Serial.println(CMD_PUMP_POT_ON(pumpID));
    /* Serial.flush();
    delay(1000);
    if(arduinoResponse() != CMD_PUMP_POT_ON(pumpID)){
        Serial.println(CMD_PUMP_POT_OFF(pumpID));
        return false;
    } */
    for (size_t i = 0; i < 15; i++)
    {
        if((readUltraSonic(PIN_US1_TRIGGER, PIN_US1_ECHO)*C_DIST_VOL) <= 10)
            break;

        delay(250);
    }
    Serial.println(CMD_PUMP_POT_OFF(pumpID));                    //CMD_PUMPx_LOW -> 0x0
    /* if(arduinoResponse() != CMD_PUMP_POT_OFF(pumpID)){
        emergency_shutdown();
        return false;
    } */
    return true;
}

int checkWaterLevel(){
    return (readUltraSonic(PIN_US2_TRIGGER, PIN_US2_ECHO)*C_DIST_VOL);
}

int checkAcidLevel(){

}

int checkFertilizerLevel(){

}

String arduinoResponse(){
    String response;

    while (Serial.available() > 0) {
        char inChar = Serial.read();   

        if (inChar != '\n') { 
        response += inChar;
        } else {
        response.trim();
        }
    }
    Serial.println(response);
    return response;
}