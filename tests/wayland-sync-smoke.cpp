// SPDX-License-Identifier: GPL-2.0-or-later
#include "autopastehelpers.h"
#include <QGuiApplication>
#include <QElapsedTimer>
#include <QThread>
#include <cassert>
#include <iostream>
static void drain(int milliseconds) {
    QElapsedTimer timer; timer.start();
    while(timer.elapsed() < milliseconds) { QCoreApplication::processEvents(); QThread::msleep(1); }
}
int main(int argc,char **argv) {
    QGuiApplication app(argc,argv);
    QObject owner; int calls=0;
    assert(KlipperAutoPaste::afterWaylandSync(&owner,[&]{++calls;}));
    drain(500); assert(calls==1);
    auto *cancelled=new QObject;
    assert(KlipperAutoPaste::afterWaylandSync(cancelled,[&]{++calls;}));
    delete cancelled; drain(100); assert(calls==1);
    std::cout << "PASS compositor ACK once; owner destruction cancels callback\n";
}
