#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <fstream>
#include <sys/stat.h>

class LinuxFile
{
private:
    int m_Handle;

public:
    LinuxFile(const char *pFile, int flags = O_RDWR)
    {
        m_Handle = open(pFile, flags);
    }

    ~LinuxFile()
    {
        if (m_Handle != -1)
            close(m_Handle);
    }

    size_t Write(const void *pBuffer, size_t size)
    {
        return write(m_Handle, pBuffer, size);
    }

    size_t Read(void *pBuffer, size_t size)
    {
        return read(m_Handle, pBuffer, size);
    }

    size_t Write(const char *pText)
    {
        return Write(pText, strlen(pText));
    }

    size_t Write(int number)
    {
        char szNum[32];
        snprintf(szNum, sizeof(szNum), "%d", number);
        return Write(szNum);
    }

    static bool Exist(const char* pFile)
    {
        std::ifstream f(pFile);
        if (f.good()) {
            f.close();
            return false;
        } else {
            f.close();
            return true;
        }
    }
};

class LinuxGPIOExporter
{
protected:
    int m_Number;

public:
    LinuxGPIOExporter(int number)
        : m_Number(number)
    {
        LinuxFile("/sys/class/gpio/export", O_WRONLY).Write(number);
    }

    ~LinuxGPIOExporter()
    {
        LinuxFile("/sys/class/gpio/unexport",
                O_WRONLY).Write(m_Number);
    }
};

class LinuxGPIO : public LinuxGPIOExporter
{
public:
    LinuxGPIO(int number)
        : LinuxGPIOExporter(number)
    {
    }

    void SetValue(bool value)
    {
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/value", m_Number);
        LinuxFile(szFN).Write(value ? "1" : "0");
    }

    void SetDirection(bool isOutput)
    {
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/direction", m_Number);
        LinuxFile(szFN).Write(isOutput ? "out" : "in");
    }

    int GetValue()
    {
        char value_str[3];
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/value", m_Number);
        LinuxFile(szFN).Read(&value_str[0], 3);
        return(atoi(value_str));
    }
};

int main(int argc, char *argv[])
{
    LinuxGPIO led_red(24);
    LinuxGPIO led_green(23);
    LinuxGPIO led_white(18);
    LinuxGPIO led_blue(17);

    LinuxGPIO button_1(10);
    LinuxGPIO button_2(27);
    LinuxGPIO button_3(22);

    led_red.SetDirection(true);
    led_green.SetDirection(true);
    led_white.SetDirection(true);
    led_blue.SetDirection(true);

    button_1.SetDirection(false);
    button_2.SetDirection(false);
    button_3.SetDirection(false);

    led_blue.SetValue(false);
    led_white.SetValue(false);
    led_green.SetValue(false);
    led_red.SetValue(false);

    int key[4], old_key[4];
    int cnt = 4;
    int b1, b2, b3, last_b1=1, last_b2=1, last_b3=1;

    if(LinuxFile::Exist("/tmp/klucz.key")) // poproś o stworzenie klucza
    {
        printf("Stwórz klucz naciskając przyciski...\n");
        printf("Klucz musi być odpowiednio długi więc\n");
        printf("Wpisuj kod aż nie zapali się czerwona dioda...\n");

        while(cnt)
        {
            b1 = button_1.GetValue();
            b2 = button_2.GetValue();
            b3 = button_3.GetValue();
            if(b1 =! last_b1 && !b1)
                key[--cnt] = 1;
            else if(b2 =! last_b2 && !b2)
                key[--cnt] = 2;
            else if(b3 =! last_b3 && !b3)
                key[--cnt] = 3;
            last_b1 = b1;
            last_b2 = b2;
            last_b3 = b3;
            if(cnt==3) led_blue.SetValue(true);
            if(cnt==2) led_white.SetValue(true);
            if(cnt==1) led_green.SetValue(true);
            if(cnt==0) led_red.SetValue(true);
            usleep(100*1000);
        }

        LinuxFile("/tmp/klucz.key", O_RDWR | O_CREAT).Write(key, 4*sizeof(int));
        printf("Zapisano klucz!\n");
        sleep(1);
    }
    else  // klucz został stworzony, poproś o jego wpisanie
    {
        printf("Podaj klucz naciskając przyciski, aby odczytać wiadomość.\n");
        LinuxFile("/tmp/klucz.key").Read(old_key, 4*sizeof(int));

        while(cnt)
        {
            b1 = button_1.GetValue();
            b2 = button_2.GetValue();
            b3 = button_3.GetValue();
            if(b1 =! last_b1 && !b1)
                key[--cnt] = 1;
            else if(b2 =! last_b2 && !b2)
                key[--cnt] = 2;
            else if(b3 =! last_b3 && !b3)
                key[--cnt] = 3;
            last_b1 = b1;
            last_b2 = b2;
            last_b3 = b3;
            usleep(100*1000);
        }

        bool same = true;
        for(int i = 0; i < 4; i++)
          if(key[i] != old_key[i]) same = false;

        if(same)
        {
            led_blue.SetValue(true);
            led_white.SetValue(true);
            led_green.SetValue(true);
            led_red.SetValue(true);
            remove("/tmp/klucz.key");
            printf("Wiadomość: udało Ci się zapamiętać kod - jestś geniuszem!\n");
            sleep(3);
        }
        else
        {
            printf("Błędny kod - głupku!\n");
        }
    }
    led_blue.SetValue(false);
    led_white.SetValue(false);
    led_green.SetValue(false);
    led_red.SetValue(false);
    return 0;
}
