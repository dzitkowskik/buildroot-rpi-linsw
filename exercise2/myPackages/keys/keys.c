#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <fstream>
#include <sys/stat.h>
#include <poll.h>

class LinuxFile
{
private:
    int m_Handle;

public:
    LinuxFile()
    {
        m_Handle = -1;
    }

    LinuxFile(const char *pFile, int flags = O_RDWR)
    {
        m_Handle = open(pFile, flags);
    }

    ~LinuxFile()
    {
        if (m_Handle != -1)
        {
            close(m_Handle);
        }
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

    int GetHandle()
    {
        return m_Handle;
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
private:
    static const int poll_timeout = -1;
    LinuxFile* valueFile;
public:
    LinuxGPIO(int number)
        : LinuxGPIOExporter(number)
    {
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/value", number);
        valueFile = new LinuxFile(szFN);
    }

    ~LinuxGPIO()
    {
        delete valueFile;
    }

    void SetValue(bool value)
    {
        valueFile->Write(value ? "1" : "0");
    }

    void SetDirection(bool isOutput)
    {
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/direction", m_Number);
        LinuxFile(szFN).Write(isOutput ? "out" : "in");
    }

    void SetEdge(const char* edge)
    {
        char szFN[128];
        snprintf(szFN, sizeof(szFN),
            "/sys/class/gpio/gpio%d/edge", m_Number);
        LinuxFile(szFN).Write(edge);
    }

    int GetValue()
    {
        char value_str[3];
        valueFile->Read(&value_str[0], 3);
        return(atoi(value_str));
    }

    LinuxFile* GetValueFile()
    {
        return valueFile;
    }

    static int WaitChange(LinuxGPIO** gpios, const int cnt)
    {
        struct pollfd pFiles[cnt];
        for(int i = 0; i < cnt; i++)
        {
          gpios[i]->GetValue();
          pFiles[i].fd = gpios[i]->GetValueFile()->GetHandle();
          pFiles[i].events = POLLPRI;
          pFiles[i].revents = 0;
        }

        int res = poll(pFiles, cnt, poll_timeout);

        if (res < 0) fprintf(stderr, "poll error!\n");
        if (res == 0) printf("poll timeout!\n");

        for(int i = 0; i < cnt; i++)
          if(pFiles[i].revents & POLLPRI) return i+1;
        return 0;
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

    button_1.SetEdge("rising");
    button_2.SetEdge("rising");
    button_3.SetEdge("rising");

    led_blue.SetValue(false);
    led_white.SetValue(false);
    led_green.SetValue(false);
    led_red.SetValue(false);

    int key[4], old_key[4];
    int cnt = 4;
    int b1, b2, b3, last_b1=1, last_b2=1, last_b3=1;

    LinuxGPIO** buttons = new LinuxGPIO*[3];
    buttons[0] = &button_1;
    buttons[1] = &button_2;
    buttons[2] = &button_3;

    if(LinuxFile::Exist("/tmp/klucz.key")) // poproś o stworzenie klucza
    {
        printf("Stwórz klucz naciskając przyciski...\n");
        printf("Klucz musi być odpowiednio długi więc\n");
        printf("Wpisuj kod aż nie zapali się czerwona dioda...\n");

        while(cnt)
        {
            int button = LinuxGPIO::WaitChange(buttons, 3);

            if(button)
            {
                printf("Pressed button %d\n", button);
                key[--cnt] = button;
                if(cnt==3) led_blue.SetValue(true);
                if(cnt==2) led_white.SetValue(true);
                if(cnt==1) led_green.SetValue(true);
                if(cnt==0) led_red.SetValue(true);
                usleep(100*1000);
            }
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
            int button = LinuxGPIO::WaitChange(buttons, 3);

            if(button)
            {
                printf("Pressed button %d\n", button);
                key[--cnt] = button;
                usleep(100*1000);
            }
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

    delete buttons;
    return 0;
}
