# lider-ahenk-remote-access-plugin

**Lider Ahenk** is an open source project which provides solutions to manage, monitor and audit unlimited number of different systems and users on a network.

Lider Ahenk remote-access plugin provides a VNC (Virtual Network Computing) client which allow users to connect to Ahenk-installed machines with desktop sharing capabilities.

This documentation **only** covers plugin related topics. To learn about core projects, please see other lider ahenk projects section.

## Setup Development Environment

> We use Eclipse for Lider and Lider Console related development. See these documentation [here](https://github.com/Pardus-Kurumsal/lider-console/wiki/01.-Setup-Development-Environment) and [here](https://github.com/Pardus-Kurumsal/lider/wiki/01.-Setup-Development-Environment) to setup Eclipse IDE with Lider and Lider Console projects imported.

1. Clone the plugin project by running `git clone https://github.com/Pardus-Kurumsal/lider-ahenk-remote-access-plugin.git`.
2. Open Eclipse and import the plugin project into Eclipse as 'Existing Maven Projects'.

## How to Build?

#### Manual build

1. Change directory to *lider-console-remote-access-dependencies/* and run `mvn clean p2:site` to (re)generate third party dependencies. This step will convert **non-OSGI** third party jar files to OSGI bundles.
2. After dependency generation, run `mvn jetty:run` to start jetty server. This will allow Tycho to consume dependencies from the server (localhost) since Tycho can't use local repositories yet.
3. Head back to project root directory and run `mvn clean install -DskipTests`.

#### Easy build

1. Instead of manually building, just run `build-plugin.sh` under the **scripts/** directory.

> **Warning**: Make sure port 8080 is available before running the script since jetty uses this port by default.

## How to Run?

Plugin project consists of three sub-modules (for **Lider**, **Lider Console** and **Ahenk**). Each sub-module is its own plugin that needs to be handled separately. Below is an explanation regarding how to run each sub-module:

#### Lider

> **Prerequisite**: Make sure you have a running Karaf container on which Lider core components installed. See [this documentation](https://github.com/Pardus-Kurumsal/lider/wiki/02.-Building-&-Running) for how to run Lider on Karaf container.

1. Type `feature:repo-add  mvn:tr.org.liderahenk/lider-remote-access-feature/1.0.0/xml/features` on Karaf shell. This will add plugin repository to the Karaf instance.
2. Again on Karaf shell, run `feature:install lider-remote-access` to install and run plugin bundles.
3. Use `log:tail` and `plugin:list` commands to ensure the plugin is installed and working properly.

#### Lider Console

> **Prerequisite**: Make sure you have a running Lider Console application. See [this documentation](https://github.com/Pardus-Kurumsal/lider-console/wiki/02.-Building-&-Running) for how to run Lider Console on Eclipse.

1. Open Eclipse, go to 'Run --> Debug Configurations' menu and on 'Plugins' tab, select _lider-console-remote-access_
2. Click 'Add Required Plugins' button to add any plugins the project depend on.
3. Finally you can run Lider Console as explained in its [documentation](https://github.com/Pardus-Kurumsal/lider-console/wiki/02.-Building-&-Running).

#### Ahenk

**TODO**

## Contribution

We encourage contributions to the project. To contribute:

* Fork the project and create a new bug or feature branch.
* Make your commits with clean, understandable comments
* Perform a pull request

## Other Lider Ahenk Projects

* [Lider Console](https://github.com/Pardus-Kurumsal/lider-console): Administration console built as Eclipse RCP project.
* [Ahenk](https://github.com/Pardus-Kurumsal/ahenk): Agent service running on remote machines.
* [Lider Ahenk Installer](https://github.com/Pardus-Kurumsal/lider-ahenk-installer): Installation wizard for Ahenk and Lider (and also its LDAP, database, XMPP servers).
* [Lider Ahenk Archetype](https://github.com/Pardus-Kurumsal/lider-ahenk-archetype): Maven archetype for easy plugin development.

## License

Lider Ahenk and its sub projects are licensed under the [LGPL v3](https://github.com/Pardus-Kurumsal/lider/blob/master/LICENSE).
