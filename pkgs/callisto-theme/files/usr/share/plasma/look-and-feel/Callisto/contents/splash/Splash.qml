import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "black"

    property int stage

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true;
        } else if (stage == 5) {
            introAnimation.target = busyIndicator;
            introAnimation.from = 1;
            introAnimation.to = 0;
            introAnimation.running = true;
        }
    }

    Item {
        id: content
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent
        opacity: 0

        Image {
            id: logo
            readonly property real size: Kirigami.Units.gridUnit * 10

            anchors.centerIn: parent

            // Raise the logo a little bit
            anchors.verticalCenterOffset: -Kirigami.Units.gridUnit * 3

            asynchronous: true
            source: "images/logo.svg"

            sourceSize.width: size
            sourceSize.height: size
        }

        Image {
            id: busyIndicator
            y: parent.height - (parent.height - logo.y) / 2 - height / 2
            anchors.horizontalCenter: parent.horizontalCenter

            asynchronous: true
            source: "images/spinner.svg"

            sourceSize.width: Kirigami.Units.gridUnit * 3
            sourceSize.height: Kirigami.Units.gridUnit * 3
            RotationAnimator on rotation {
                id: rotationAnimator
                from: 0
                to: 360
                duration: 1500
                loops: Animation.Infinite
                running: Kirigami.Units.longDuration > 1
            }
        }

        Row {
            spacing: Kirigami.Units.largeSpacing
            anchors {
                bottom: parent.bottom
                right: parent.right
                margins: Kirigami.Units.gridUnit
            }
            Text {
                color: "#eff0f1"
                anchors.verticalCenter: parent.verticalCenter
                text: i18ndc("plasma_lookandfeel_org.kde.lookandfeel", "Plasma logo credit", "Plasma made by KDE")
                Accessible.name: text
                Accessible.role: Accessible.StaticText
            }
            Image {
                asynchronous: true
                source: "images/kde.svg"
                sourceSize.height: Kirigami.Units.gridUnit * 2
                sourceSize.width: Kirigami.Units.gridUnit * 2
            }
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }
}