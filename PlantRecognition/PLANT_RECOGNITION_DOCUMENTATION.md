# Plantrecognition_Smartgrow
In diesem Repository ist der Code fuer die Erkennung von Pflanzen (speziell Krautern) mit einem CNN hinterlegt. 

## Hinweise zum ImageDownloader
Im Ordner ImageDownloader ist ein python script, mit welchen automatisch Suchanfragen durchgefuehrt werden koennen und daraufhin eine definierte Anzahl an Bildern gedownloaded werden.
Im .env file ist ein serpapi key zu hinterlegen, da serpapi als Schnittstelle zu einer Suchmaschine verwendet wird. 
Einen key bekommt man indem man sich bei serpapi registriert. [Link zur SerpAPI Website](https://serpapi.com/)

Im python skript sind einige weitere Dinge zu beachten:
  1. In Zeile 39 kann der Name des CSV-Files festgelegt werden, in welchen die Quellen der Bilder abgespeichert werden.
  2. In Zeile 47 bis 52 kann die Suchanfrage spezifiziert werden
  3. In Zeile 67 kann das Verzeichnis angegeben werden, in dem die Bilder gespeichert werden

## Ordner Notebooks
Das Notebook iLoveBasilAndParsley.ipynb dokumentiert den Entwicklungsprozess.
Zunaechst wurde versucht ein Modell von Grundauf neu zu entwickeln. Hierfür war die vorhandene Datenmenge jedoch nicht ausreichend.
In der zweiten großen Entwicklungsphase hat man deshalb versucht auf ein vortrainiertes Modell zurück zu greifen.
Es wurde die Faltungsbasis des VGG16-Modells verwendet und um einen Klassifizierer erweitert. Diese Struktur wurde anschließend mit dem Datensatz neu trainiert und optimiert.
Hiermit konnten zufriedenstellende Ergebnisse erzielt werden.

Im Transfer.ipynb ist der Versuch dokumentiert das Modell in ein tensorflow-lite Modell zu überführen, was für den Einsatz auf eingebetteten Systemen besser wäre. So könnte Speicher- sowie Rechenintensität vermindert werden. Die Überführung sorgte jedoch für einen deutlichen Abfall in der Genauigkeit des Modells unter gleichen Testbedingnungen.
Es wurde sich dazu entschieden das Modell in seiner Ursprungsform auf einem RaspberryPi zu betreiben. Sollte das Modell jedoch erweitert werden oder auf einem kleineren Mikrocontroller betrieben werden, sollte man sich diesen Arbeitsschritt noch einmal genauer ansehen und versuchen das Modell zu verkleinern / zu quantisieren.
In diesem Zusammenhang verweise ich auf das folgende Paper: C. Alippi, S. Disabato and M. Roveri, "Moving Convolutional Neural Networks to Embedded Systems: The AlexNet and VGG-16 Case" (https://ieeexplore.ieee.org/document/8480072)

## Hinweise zu models
In diesem Ordner findet sich eine Markdown-Datein in welcher ein Download-Link bereitgestellt wird, über welchen das finale Keras-Model sowie ein Tf-Lite Modell bezogen werden kann.
Das tf-Lite Model ist lediglich fuer Weiterentwicklungszwecke veroeffentlicht, es erzielt in dieser Form keine erwünschte Genauigkeit bei der Klassifikation.

Das Keras-Modell hingegen erzielte auf den Test-Datensatz eine  Genauigkeit von 95 % und wurde auch schon auf einem RaspberryPi eingesetzt.

## Hinweise zu Dataset
Der im Projekt verwendete Datensatz kann ueber einen Download-Link bezogen werden. Beim Download der Bilder wurde darauf geachtet, dass diese alle der Creative Commons license unterliegen.
Des Weiteren ist ein Jupyter-Notebook beigefügt, in welchem dokumentiert ist, wie der Datensatz aufgeteilt wurde.

## RaspberryPi
Hier sind zwei Testskripte beigefuegt wie das Modell auf einem RaspberryPi verwendet werden könnte.

## Weitere Dokumentation
Weitere Dokumentation findet sich in den Notebooks selbst.

## Allgemein verwendete Quellen zur Umsetzung dieses Projekts
Ian Goodfellow and Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016

François Chollet, Deep Learning mit Python und Keras, mitp, 2018
