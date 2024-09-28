#include <Arduino.h>

class Sensor
{
private:
    String Mac;
    int Pot;

    int MinMoisture;
    int MaxMoisture;
    int MinConductivity;
    int MaxConductivity;
    float MinPh;
    float MaxPh;

    float temperature;
    float ph;
    int moisture;
    int light;
    int conductivity;
    int battery;

public:
    String getMac()
    {
        return this->Mac;
    }

    void setMac(String Mac)
    {
        this->Mac = Mac;
    }

    int getPot()
    {
        return this->Pot;
    }

    void setPot(int Pot)
    {
        this->Pot = Pot;
    }

    int getMinMoisture()
    {
        return this->MinMoisture;
    }

    void setMinMoisture(int MinMoisture)
    {
        this->MinMoisture = MinMoisture;
    }

    int getMaxMoisture()
    {
        return this->MaxMoisture;
    }

    void setMaxMoisture(int MaxMoisture)
    {
        this->MaxMoisture = MaxMoisture;
    }

    int getMinConductivity()
    {
        return this->MinConductivity;
    }

    void setMinConductivity(int MinConductivity)
    {
        this->MinConductivity = MinConductivity;
    }

    int getMaxConductivity()
    {
        return this->MaxConductivity;
    }

    void setMaxConductivity(int MaxConductivity)
    {
        this->MaxConductivity = MaxConductivity;
    }

    float getMinPh()
    {
        return this->MinPh;
    }

    void setMinPh(float MinPh)
    {
        this->MinPh = MinPh;
    }
    
    float getMaxPh()
    {
        return this->MaxPh;
    }

    void setMaxPh(float MaxPh)
    {
        this->MaxPh = MaxPh;
    }

    float gettemperature()
    {
        return this->temperature;
    }

    void settemperature(float temperature)
    {
        this->temperature = temperature;
    }
    
    float getph()
    {
        return this->ph;
    }

    void setph(float ph)
    {
        this->ph = ph;
    }

    int getmoisture()
    {
        return this->moisture;
    }

    void setmoisture(int moisture)
    {
        this->moisture = moisture;
    }

    int getlight()
    {
        return this->light;
    }

    void setlight(int light)
    {
        this->light = light;
    }

    int getconductivity()
    {
        return this->conductivity;
    }

    void setconductivity(int conductivity)
    {
        this->conductivity = conductivity;
    }

    int getbattery()
    {
        return this->battery;
    }

    void setbattery(int battery)
    {
        this->battery = battery;
    }
};