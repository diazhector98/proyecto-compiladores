//
//  ViewController.swift
//  PlusPlusC
//
//  Created by Héctor Díaz Aceves on 5/28/21.
//  Copyright © 2021 Héctor Díaz Aceves. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var compileButton: UIButton!
    @IBOutlet weak var runButton: UIButton!
    @IBOutlet weak var cleanButton: UIButton!
    @IBOutlet weak var codeInputTextView: UITextView!
    @IBOutlet weak var outputTextView: UITextView!
    
    //Flask API endpoints
    let APIUrl: String = "http://127.0.0.1:5000/"
    let APIUrlPOSTCompile: String = "http://127.0.0.1:5000/compileFile"
    let APIUrlPOSTRun: String = "http://127.0.0.1:5000/runFile"
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let tap = UITapGestureRecognizer(target: self.view, action: #selector(UIView.endEditing))
        view.addGestureRecognizer(tap)
        setUpElementsUI()
    }
    
    private func setUpElementsUI() {
        compileButton.layer.cornerRadius = compileButton.frame.height/2
        runButton.layer.cornerRadius = runButton.frame.height/2
        cleanButton.layer.cornerRadius = cleanButton.frame.height/2
        codeInputTextView.layer.cornerRadius = 10
        outputTextView.layer.cornerRadius = 10
    }
    
    @IBAction func compileButtonPressed(_ sender: Any) {
        let codeInput = String(codeInputTextView.text)
        
        guard let url = URL(string: APIUrlPOSTCompile) else {
            print("Error: Couldn't reach Flask API: APIUrlPOSTCompile")
            return
        }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        
        let params = ["code": codeInput]
        
        do {
            let data = try JSONSerialization.data(withJSONObject: params, options: .init())
            urlRequest.httpBody = data
            urlRequest.setValue("application/json", forHTTPHeaderField: "content-type")
            
            URLSession.shared.dataTask(with: urlRequest) { (data, response, error) in
                guard let data = data else { return }
                do {
                    let json = try JSONSerialization.jsonObject(with: data, options: [])
                    if let dict = json as? [String: Any] {
                        if let value = dict["compiler"] as? String {
                            DispatchQueue.main.async {
                                self.outputTextView.text = value
                            }
                        }
                    }
                } catch {
                    print("Error fetching key: value")
                }
            }.resume()
        } catch {
            print("Error fetching data.")
        }
    }
    
    @IBAction func runButtonPressed(_ sender: Any) {
        guard let url = URL(string: APIUrlPOSTRun) else {
            print("Error: Couldn't reach Flask API: APIUrlPOSTRun")
            return
        }
        
        let outputResult = String(outputTextView.text)
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        
        let params = ["compilerResult": outputResult]
        
        do {
            let data = try JSONSerialization.data(withJSONObject: params, options: .init())
            urlRequest.httpBody = data
            urlRequest.setValue("application/json", forHTTPHeaderField: "content-type")
            
            URLSession.shared.dataTask(with: urlRequest) { (data, response, error) in
                guard let data = data else { return }
                do {
                    let json = try JSONSerialization.jsonObject(with: data, options: [])
                    if let dict = json as? [String: Any] {
                        if let value = dict["result"] as? String {
                            self.outputTextView.text = ""
                            DispatchQueue.main.async {
                                if value == "" {
                                    print("viene vacio")
                                }
                                self.outputTextView.text = value
                            }
                        }
                    }
                } catch {
                    print("Error fetching key: value")
                }
            }.resume()
        } catch {
            print("Error fetching data.")
        }
    }
    
    @IBAction func cleanButtonPressed(_ sender: Any) {
        codeInputTextView.text = ""
        outputTextView.text = ""
    }
}

