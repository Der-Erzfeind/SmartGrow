#include <Arduino.h>

#ifndef control.h
    #define control.h  

    #define PIN_ARDUINO_PWR 2
    #define PIN_US_WATER_TRIGGER 12
    #define PIN_US_WATER_ECHO 13
    #define PIN_US_FERTILIZER_TRIGGER 33
    #define PIN_US_FERTILIZER_ECHO 25
    #define PIN_US_ACID_TRIGGER 27
    #define PIN_US_ACID_ECHO 26
    #define PIN_PH_PO 14



    //#define CMD_PUMP_POT_OFF(pot) "CMD_PUMP" #pot "_OFF"      --> cannot take input value, therefore implemented in addWater function
    #define CMD_PUMP_WATER_OFF "CMD_PUMP4_OFF"
    #define CMD_PUMP_FERTILIZER_OFF "CMD_PUMP5_OFF"
    #define CMD_PUMP_ACID_OFF "CMD_PUMP6_OFF"

    //#define CMD_PUMP_POT_ON(pot) "CMD_PUMP" #pot "_ON"        --> cannot take input value, therefore implemented in addWater function
    #define CMD_PUMP_WATER_ON "CMD_PUMP4_ON"
    #define CMD_PUMP_FERTILIZER_ON "CMD_PUMP5_ON"
    #define CMD_PUMP_ACID_ON "CMD_PUMP6_ON"

    #define ACK_PUMP_POT_OFF(pot) "ACK_PUMP" #pot "_OFF"
    #define ACK_PUMP_WATER_OFF "ACK_PUMP4_OFF"
    #define ACK_PUMP_FERTILIZER_OFF "ACK_PUMP5_OFF"
    #define ACK_PUMP_ACID_OFF "ACK_PUMP6_OFF"

    #define ACK_PUMP_POT_ON(pot) "ACK_PUMP" #pot "_ON"
    #define ACK_PUMP_WATER_ON "ACK_PUMP4_ON"
    #define ACK_PUMP_FERTILIZER_ON "ACK_PUMP5_ON"
    #define ACK_PUMP_ACID_ON "ACK_PUMP6_ON"

    #define C_TIME_VOL 0.05 * 1000
    #define C_DIST_VOL 3
    #define C_PH_VOL 4


    void emergency_shutdown();
    void initHardware();
    float readUltraSonic(int trigger_pin, int echo_pin);
    void bubbleSort(int arr[], int n);
    float findMedian(int arr[], int n);
    float read_PH();
    bool addWater(int ml);
    bool addFertilizer(int ml);
    bool correctPH(float ph);
    bool waterPlant(int pumpID);
    String arduinoResponse();

#endif