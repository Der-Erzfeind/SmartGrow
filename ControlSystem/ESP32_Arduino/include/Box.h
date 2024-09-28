#include <Arduino.h>

class Box{

private:

    int volmix;
    int volwater;
    int volfertilizer;
    int volacid;

public:

    int getvolMix()
    {
        return this->volmix;
    }

    void setvolMix(int volmix)
    {
        this->volmix = volmix;
    }

    int getvolWater()
    {
        return this->volwater;
    }

    void setvolWater(int volwater)
    {
        this->volwater = volwater;
    }

    int getvolFertilizer()
    {
        return this->volfertilizer;
    }

    void setvolFertilizer(int volfertilizer)
    {
        this->volfertilizer = volfertilizer;
    }

    int getvolAcid()
    {
        return this->volacid;
    }

    void setvolAcid(int volacid)
    {
        this->volacid = volacid;
    }
};