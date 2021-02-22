import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'yo App',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        visualDensity: VisualDensity
            .adaptivePlatformDensity, // Changes visuals based on platform (IOS or Android)
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  // syntax for 'state' classes
  String text = '';

  void changeText(String text) {
    this.setState(() {
      this.text = text;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('yo')),
        body: Column(children: <Widget>[
          TextInputWidget(this.changeText),
          Text(this.text)
        ]));
  }
}

class TextInputWidget extends StatefulWidget {
  // The "state" is determined by the user's actions
  // Takes constructor arguments
  final Function(String) callback;

  TextInputWidget(this.callback);

  @override
  _TextInputWidgetState createState() => _TextInputWidgetState();
}

class _TextInputWidgetState extends State<TextInputWidget> {
  final controller = TextEditingController();
  // Handles state and rendering of widget
  @override
  void dispose() {
    super.dispose();
    controller.dispose(); // Not this.controller.dispose();?
  }

  void click() {
    widget.callback(controller.text); // widget. accesses TextInputWidget
    controller.clear(); // clears text field
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
        controller: this.controller,
        decoration: InputDecoration(
            prefixIcon: Icon(Icons.message),
            labelText: 'Type a ticker.',
            suffixIcon: IconButton(
                icon: Icon(Icons.send),
                splashColor: Colors.orange,
                tooltip: 'Post message',
                onPressed: () => {})));
  }
}
