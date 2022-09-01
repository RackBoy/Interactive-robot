#include "Arduino.h"
#include "Oscillator.h"
#include "NeoSWSerial.h"
#include <Servo.h>
/*
         ---------------
        |     O   O     |
        |---------------|
YR 2<== |               | <== YL 3
         ---------------
            ||     ||
            ||     ||
RR 0==^   -----   ------  v== RL 1
         |-----   ------|
*/

/* Hardware interface mapping*/

#define SOFTWARE_RXD A2 //Software implementation of serial interface (audio module driver interface)
#define SOFTWARE_TXD A3
#define MY1690_PIN 8
#define HT6871_PIN 7
NeoSWSerial mp3Serial(SOFTWARE_RXD, SOFTWARE_TXD);

#define YL_PIN 10 
#define YR_PIN 9  
#define RL_PIN 12 
#define RR_PIN 6  

#define N_SERVOS 4
#define INTERVALTIME 10.0
#define CENTRE 90
#define AMPLITUDE 30
#define ULTRA_HIGH_RATE 0.3
#define HIGH_RATE 0.5
#define MID_RATE 0.7
#define LOW_RATE 1.0
#define ULTRA_LOW_RATE 1.5

int t=495;
char mov_=""; //moviento adelante

Oscillator servo[N_SERVOS];

#define CENTRE 90

unsigned long final_time;
unsigned long interval_time;
int oneTime;
int iteration;
float increment[N_SERVOS];
int oldPosition[] = {CENTRE, CENTRE, CENTRE, CENTRE};


class MY1690_16S{
public:
    int volume;
    String playStatus[5] = {"0", "1", "2", "3", "4"}; // STOP PLAYING PAUSE FF FR

    /* Music Playing Choice*/ 
    void playSong(unsigned char num, unsigned char vol){
        setVolume(vol);
        setPlayMode(4);
        CMD_SongSelet[4] = num;
        checkCode(CMD_SongSelet);
        mp3Serial.write(CMD_SongSelet, 7);
        delay(50);
    }
    /* Get playback status*/
    String getPlayStatus(){
        mp3Serial.write(CMD_getPlayStatus, 5);
        delay(50);
        return getStatus();
    }
    /* Get status*/
    String getStatus(){
        String statusMp3 = "";
        while (mp3Serial.available()){
            statusMp3 += (char)mp3Serial.read();
        }
        return statusMp3;
    }
    /* Stop broadcasting*/
    void stopPlay(){
        setPlayMode(4);
        mp3Serial.write(CMD_MusicStop, 5);
        delay(50);
    }
    /* Volume setting*/
    void setVolume(unsigned char vol){
        CMD_VolumeSet[3] = vol;
        checkCode(CMD_VolumeSet);
        mp3Serial.write(CMD_VolumeSet, 6);
        delay(50);
    }
    /* Voice Enhancement*/
    void volumePlus(){
        mp3Serial.write(CMD_VolumePlus, 5);
        delay(50);
    }
    /* Lower volume*/
    void volumeDown(){
        mp3Serial.write(CMD_VolumeDown, 5);
        delay(50);
    }

    void setPlayMode(unsigned char mode){
        CMD_PlayMode[3] = mode;
        checkCode(CMD_PlayMode);
        mp3Serial.write(CMD_PlayMode, 6);
        delay(50);
    }

    void checkCode(unsigned char *vs){
        int val = vs[1];
        int i;
        for (i = 2; i < vs[1]; i++)
            val = val ^ vs[i];
        vs[i] = val;
    }

    void ampMode(int p, bool m){
        pinMode(p, OUTPUT);
        if (m)
            digitalWrite(p, HIGH);
        
        else
            digitalWrite(p, LOW);
    }

    void init(){
        ampMode(HT6871_PIN, HIGH);
        stopPlay();
        volume = 15;
    }

private:
    byte CMD_MusicPlay[5] = {0x7E, 0x03, 0x11, 0x12, 0xEF};
    byte CMD_MusicStop[5] = {0x7E, 0x03, 0x1E, 0x1D, 0xEF};
    byte CMD_MusicNext[5] = {0x7E, 0x03, 0x13, 0x10, 0xEF};
    byte CMD_MusicPrev[5] = {0x7E, 0x03, 0x14, 0x17, 0xEF};
    byte CMD_VolumePlus[5] = {0x7E, 0x03, 0x15, 0x16, 0xEF};
    byte CMD_VolumeDown[5] = {0x7E, 0x03, 0x16, 0x15, 0xEF};
    byte CMD_VolumeSet[6] = {0x7E, 0x04, 0x31, 0x00, 0x00, 0xEF};
    byte CMD_PlayMode[6] = {0x7E, 0x04, 0x33, 0x00, 0x00, 0xEF};
    byte CMD_SongSelet[7] = {0x7E, 0x05, 0x41, 0x00, 0x00, 0x00, 0xEF};
    byte CMD_getPlayStatus[5] = {0x7E, 0x03, 0x20, 0x23, 0xEF};
} mp3;

bool delays(unsigned long ms){
    for (unsigned long i = 0; i < ms; i++)
        delay(1);
    
    return false;
}

/*
    Setting the 90-degree position of the steering gear to make the penguin stand on its feet
*/
void homes(int millis_t){
    servo[0].SetPosition(90);
    servo[1].SetPosition(90);
    servo[2].SetPosition(90);
    servo[3].SetPosition(90);
    delay(millis_t);
}
bool moveNServos(int time, int newPosition[]){
    for (int i = 0; i < N_SERVOS; i++)
        increment[i] = ((newPosition[i]) - oldPosition[i]) / (time / INTERVALTIME);
    
    final_time = millis() + time;
    iteration = 1;
    while (millis() < final_time){
        interval_time = millis() + INTERVALTIME;
        oneTime = 0;
        while (millis() < interval_time){
            if (oneTime < 1){
                for (int i = 0; i < N_SERVOS; i++)
                    servo[i].SetPosition(oldPosition[i] + (iteration * increment[i]));
                
                iteration++;
                oneTime++;
            }
        }
    }
    for (int i = 0; i < N_SERVOS; i++)
        oldPosition[i] = newPosition[i];
    
    return false;
}
/*
  Walking control realization:
*/
bool walk(int steps, int T, int dir){
    int move1[] = {90, 90 + 35, 90 + 15, 90 + 15};
    int move2[] = {90 + 25, 90 + 30, 90 + 15, 90 + 15};
    int move3[] = {90 + 20, 90 + 20, 90 - 15, 90 - 15};
    int move4[] = {90 - 35, 90, 90 - 15, 90 - 15};
    int move5[] = {90 - 40, 90 - 30, 90 - 15, 90 - 15};
    int move6[] = {90 - 20, 90 - 20, 90 + 15, 90 + 15};

    int move21[] = {90, 90 + 35, 90 - 15, 90 - 15};
    int move22[] = {90 + 25, 90 + 30, 90 - 15, 90 - 15};
    int move23[] = {90 + 20, 90 + 20, 90 + 15, 90 + 15};
    int move24[] = {90 - 35, 90, 90 + 15, 90 + 15};
    int move25[] = {90 - 40, 90 - 30, 90 + 15, 90 + 15};
    int move26[] = {90 - 20, 90 - 20, 90 - 15, 90 - 15};

    if (dir == 1) //Walking forward
    {
        for (int i = 0; i < steps; i++)
            if (
                moveNServos(T * 0.2, move1) ||
                delays(50) ||
                moveNServos(T * 0.2, move2) ||
                delays(50) ||
                moveNServos(T * 0.2, move3) ||
                delays(100) ||
                moveNServos(T * 0.2, move4) ||
                delays(250) ||
                moveNServos(T * 0.2, move5) ||
                delays(100) ||
                moveNServos(T * 0.2, move6) ||
                delays(100))
                return true;
    }
    else //Walking backward
    {
        for (int i = 0; i < steps; i++)
            if (
                moveNServos(T * 0.2, move21) ||
                delays(50 / 10) ||
                moveNServos(T * 0.2, move22) ||
                delays(50) ||
                moveNServos(T * 0.2, move23) ||
                delays(100) ||
                moveNServos(T * 0.2, move24) ||
                delays(250) ||
                moveNServos(T * 0.2, move25) ||
                delays(100) ||
                moveNServos(T * 0.2, move26))
                return true;
    }
    return false;
}

int trim_rr;
int trim_rl;
int trim_yr;
int trim_yl;

void servoAttach(){
    //
    servo[0].SetTrim(trim_rr);
    servo[1].SetTrim(trim_rl);
    servo[2].SetTrim(trim_yr);
    servo[3].SetTrim(trim_yl);
   
    servo[0].attach(RR_PIN);
    servo[1].attach(RL_PIN);
    servo[2].attach(YR_PIN);
    servo[3].attach(YL_PIN);
}

bool lateral_fuerte(boolean dir, int tempo){
    if (dir){
        int move1[] = {CENTRE - 2 * AMPLITUDE, CENTRE - AMPLITUDE, CENTRE, CENTRE};
        int move2[] = {CENTRE + AMPLITUDE, CENTRE - AMPLITUDE, CENTRE, CENTRE};
        int move3[] = {CENTRE - 2 * AMPLITUDE, CENTRE - AMPLITUDE, CENTRE, CENTRE};
        if (moveNServos(tempo * LOW_RATE, move1) || delays(tempo * 2) ||
            moveNServos(tempo * ULTRA_HIGH_RATE, move2) || delays(tempo / 2) ||
            moveNServos(tempo * ULTRA_HIGH_RATE, move3) || delays(tempo))
            return true;
    }
    else{
        int move1[] = {CENTRE + AMPLITUDE, CENTRE + 2 * AMPLITUDE, CENTRE, CENTRE};
        int move2[] = {CENTRE + AMPLITUDE, CENTRE - AMPLITUDE, CENTRE, CENTRE};
        int move3[] = {CENTRE + AMPLITUDE, CENTRE + 2 * AMPLITUDE, CENTRE, CENTRE};
        if (moveNServos(tempo * LOW_RATE, move1) || delays(tempo * 2) ||
            moveNServos(tempo * ULTRA_HIGH_RATE, move2) || delays(tempo / 2) ||
            moveNServos(tempo * ULTRA_HIGH_RATE, move3) || delays(tempo))
            return true;
    }
    if (home())
        return true;
    return false;
}

bool home(){
    int move1[] = {90, 90, 90, 90};
    if (moveNServos(t, move1) || delays(t))
        return true;
    return false;
}

void servoDetach(){
    servo[0].detach();
    servo[1].detach();
    servo[2].detach();
    servo[3].detach();
}

void start(){
    mp3.stopPlay();
    delay(10);
    mp3.stopPlay();
    delay(10);
    mp3.stopPlay();
    delay(10);
    mp3.playSong(1, mp3.volume);
    mp3.setVolume(10);
    //lateral_fuerte(1,t); //movimiento de inicio   
    mp3.stopPlay();
    delay(10);
    mp3.stopPlay();
    delay(10);
    mp3.stopPlay();
    delay(10);
}


void setup(){
    Serial.begin(9600);
    
    mp3Serial.begin(9600);
    mp3.init(); 
    
    servo[0].attach(RR_PIN);
    servo[1].attach(RL_PIN);
    servo[2].attach(YR_PIN);
    servo[3].attach(YL_PIN);
    start(); //movimiento de inicio robot
    homes(100);
}

void loop(){
//este es el codigo final 
  if(Serial.available()){
    mov_=Serial.read();
  if(mov_=='F' || mov_=='f'){
    for (int i = 0; i < 2; i++) 
        walk(1, 1500, 1); //movimiento adelante
        homes(100);
  }
  else if (mov_=='B' || mov_=='b'){
    for (int i = 0; i < 2; i++)
        walk(1, 1500, 0);//movimiento atras
        homes(100);
  }
  else if(mov_=='l'){ //palabra chapie
    servoAttach();
    lateral_fuerte(1, t);
    servoDetach();
  }
}
} //fin loop
