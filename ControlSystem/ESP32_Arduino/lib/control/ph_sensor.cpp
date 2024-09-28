#include <Arduino.h>

const int pHSensorPin = 34; // ADC1 Channel 6 is GPIO34
float voltage, pH;
int buffer_arr[9];

float calibration_value = 0.15;

void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Tausche arr[j] und arr[j+1]
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

float findMedian(int arr[], int n) {
    if (n % 2 == 0) {
        // Wenn n gerade ist, den Durchschnitt der beiden mittleren Werte berechnen
        return (arr[n / 2 - 1] + arr[n / 2]) / 2.0;
    } else {
        // Wenn n ungerade ist, den mittleren Wert zurückgeben
        return arr[n / 2];
    }
}

void init_PH()
{
  pinMode(pHSensorPin, ANALOG);
  analogReadResolution(12); // Set ADC resolution to 12 bits
}

float read_PH()
{

  for(int i=0;i<9;i++)
  {
    buffer_arr[i]=analogRead(pHSensorPin);
    delay(30);
  }

  bubbleSort(buffer_arr, 9);

  float median = findMedian(buffer_arr, 9);

  voltage = median * (3.0 / 4095.0) + calibration_value;
  // Berechnung PH
//   pH = 7 + (voltage-1.5)*(4-7)/(1.7-1.5);
  
  pH = (0.07 * 7 - voltage + 1.5)/0.07;
  Serial.printf("ph is %d\n", pH);

  return pH;
}

