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
    
    @IBOutlet weak var codeInputTextView: UITextView!
    @IBOutlet weak var outputTextView: UITextView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        let tap = UITapGestureRecognizer(target: self.view, action: #selector(UIView.endEditing))
        view.addGestureRecognizer(tap)
    }

    @IBAction func compileButtonPressed(_ sender: Any) {
        let codeInput = codeInputTextView.text
        print(codeInput!)

        let parameters = ["code": codeInput]
        let url = URL(string: "www.thisismylink.com/postName.php")! //change the url
        let session = URLSession.shared
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: .prettyPrinted) // pass dictionary to nsdata object and set it as request body
        } catch let error {
            print(error.localizedDescription)
        }
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")

        let task = session.dataTask(with: request as URLRequest, completionHandler: { data, response, error in
            guard error == nil else {
                return
            }
            guard let data = data else {
                return
            }
            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: .mutableContainers) as? [String: Any] {
                    print(json)
                }
            } catch let error {
                print(error.localizedDescription)
            }
        })
        task.resume()
    }
    
    @IBAction func runButtonPressed(_ sender: Any) {
    }
    
    
    
    
}

