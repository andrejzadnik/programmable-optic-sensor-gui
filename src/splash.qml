import QtQuick 2.4

Item {
    x: 0
    y: 0
    width: 480
    height: 264
    antialiasing: true
    rotation: 0
    transformOrigin: Item.Top

    // Icon from https://www.python.org/
    Image {
        id: image1
        x: 28
        y: 185
        width: 58
        height: 54
        source: "icons/python.png"
    }

    // Icon from www.qt.io
    Image {
        id: image2
        x: 132
        y: 185
        width: 58
        height: 54
        source: "icons/Apps-Qt-icon.png"
    }

    // Icon from https://www.google.si/search?q=qml&espv=2&biw=1680&bih=952&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi_5JWeldnRAhVCFywKHadrAJsQ_AUICCgB#imgrc=LB-L0O2P_wq0SM%3A
    Image {
        id: image3
        x: 235
        y: 185
        width: 58
        height: 54
        source: "icons/qml.png"
    }

    Image {
        id: image4
        x: 320
        y: 97
        width: 152
        height: 142
        source: "icons/qrcode.png"
    }

    Text {
        id: text1
        x: 86
        y: 32
        width: 394
        height: 30
        text: qsTr("Programmable optic sensor")
        style: Text.Raised
        font.italic: false
        font.family: "Verdana"
        font.bold: true
        textFormat: Text.RichText
        wrapMode: Text.WrapAnywhere
        font.pixelSize: 25
    }

    Text {
        id: text2
        x: 356
        y: 68
        width: 80
        height: 18
        text: qsTr("Version: 0.9.1")
        font.bold: true
        font.pixelSize: 14
    }

    Text {
        id: text3
        x: 296
        y: 245
        width: 176
        height: 14
        text: qsTr("Andrej Zadnik, January 2017")
        font.pixelSize: 12
    }

    Image {
        id: image5
        x: 0
        y: 0
        width: 480
        height: 268
        opacity: 1
        clip: false
        visible: true
        z: -1
        source: "icons/splash.jpg"
    }

    Text {
        id: text4
        x: 107
        y: 65
        width: 252
        height: 26
        color: "#ea0707"
        text: qsTr("Graphical User Interface")
        styleColor: "#002b6c"
        font.italic: true
        font.bold: true
        font.pixelSize: 17
    }
}
