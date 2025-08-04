#include <atomic>
#include <chrono>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sched.h> // pid_t data type
#include <sys/select.h>
#include <thread>
#include <unistd.h> // For fork();

using namespace std;

// atomic type => ensure that variable can be safely accessed and modified.
// // 1 = Suddenly at 0%, 0 = Not at 0%
atomic<int> BAT_EMPTY(0);

// If another instance of this program is running...
const char *lockFilePath = "/tmp/bat-daemon-run";

// Checks if the file exists. (Another instance is running)
bool isRunning() {
  ifstream lockFile(lockFilePath);
  return lockFile.good();
}

// Creates file w/ PID
void createLockFile() {
  ofstream lockFile(lockFilePath);
  lockFile << getpid();
}

// Removes file.
void removeLockFile() { remove(lockFilePath); }

void send_notifs_empty() {
  string command = "notify-send 'Low Battery' 'ALERT! 0% Battery Remaining.' "
                   "-u critical -i 'battery-caution' -t 5000";

  // If battery is empty...
  while (BAT_EMPTY.load() == 1) {
    system(command.c_str());
    this_thread::sleep_for(chrono::seconds(5));
  }
}

void send_notifs_warn(const int &percent) {
  // Formulate command
  string command =
      "notify-send 'Low Battery' '" + to_string(percent) +
      "% of battery remaining.' -u critical -i 'battery-caution' -t 5000";

  // Execute command as a C-String (same contents, but compatible with C++ code)
  // "Returns a pointer to an array that contains the contents of the variable"
  system(command.c_str());
}

void send_notifs_charge(const int &percent, const int status) {
  string command;

  switch (status) {
  case 1:
    command = "notify-send 'Charging' 'Charging battery at " +
              to_string(percent) +
              "%' -u low -i 'battery-level-50-charging-symbolic' -t 5000";
    break;

  case 0:
    command = "notify-send 'Discharging' '" + to_string(percent) +
              "% remaining' -u low -i 'battery-level-70-symbolic' -t 5000";
    break;
  }

  system(command.c_str());
}

void send_notifs_full() {
  string command = "notify-send 'Battery Full' 'Battery is fully charged!' -i "
                   "'battery-full-charged' -t 5000";
  system(command.c_str());
}

// Checks battery info. (Charging, Discharging, etc.)
void battery() {
  int OLD_BAT_PERCENT = 100; // Maxing out to prevent bugs
  int CHARGE = 0;            // 1 = Charging, 0 = Discharging
  int BAT_FULL = 0;          // 1 = Full, 0 = Not Full

  while (true) {
    int BAT_WARN = 35;
    // Read and Grab File Info:

    // ifstream (input file stream) class: operates on files (I/O)
    ifstream BAT_STATUS_FILE("/sys/class/power_supply/BAT0/status");
    string BAT_STATUS;

    ifstream BAT_PERCENT_FILE("/sys/class/power_supply/BAT0/capacity");
    int BAT_PERCENT;

    // If it can't extract info, exit.
    if (!(BAT_PERCENT_FILE >> BAT_PERCENT) ||
        !(BAT_STATUS_FILE >> BAT_STATUS)) {
      exit(EXIT_FAILURE);
    }

    // Timing:
    // timeval = Time Value accurate from microseconds to years.
    struct timeval tv;

    // Set intervals: 0sec + 100 milsec.
    tv.tv_sec = 0;
    tv.tv_usec = 100000;

    // If the actual battery is charging, update all values
    if (BAT_STATUS == "Charging") {
      if (BAT_PERCENT < 99 && CHARGE == 0) {
        CHARGE = 1;
        OLD_BAT_PERCENT = BAT_PERCENT;
        BAT_FULL = 0;
        send_notifs_charge(BAT_PERCENT, CHARGE);

      } else if (BAT_PERCENT >= 99 && BAT_FULL == 0) {
        BAT_FULL = 1;
        CHARGE = 1;
        send_notifs_full();

      } else if (BAT_PERCENT > OLD_BAT_PERCENT) {
        OLD_BAT_PERCENT = BAT_PERCENT;
      }

      if (BAT_EMPTY == 1) {
        BAT_EMPTY.store(0);
      }
    }

    // If the actual battery is discharging, update all values
    if (BAT_STATUS == "Discharging") {
      if (CHARGE == 1) {
        CHARGE = 0;
        send_notifs_charge(BAT_PERCENT, CHARGE);

      } else if (BAT_PERCENT < 99 && BAT_FULL == 1) {
        BAT_FULL = 0;

      } else if (BAT_PERCENT <= BAT_WARN && BAT_PERCENT < OLD_BAT_PERCENT) {
        OLD_BAT_PERCENT = BAT_PERCENT;
        send_notifs_warn(BAT_PERCENT);
      }

      // Change value of BAT_EMPTY (alert notification)
      if (BAT_PERCENT == 0 && BAT_EMPTY == 0) {
        BAT_EMPTY.store(1);
      }
    }

    select(0, NULL, NULL, NULL, &tv);
  }
}

// Initializer
int main() {
  // Change directory to root
  chdir("/");

  // Redirects all streams to /dev/null
  freopen("/dev/null", "r", stdin);
  freopen("/dev/null", "w", stdout);
  freopen("/dev/null", "w", stderr);

  if (isRunning()) {
    ifstream lockFile(lockFilePath);
    int pid;

    lockFile >> pid;

    removeLockFile();

    kill(pid, 1);
  }

  createLockFile();

  battery();

  thread background(send_notifs_empty);

  return 0;
}
