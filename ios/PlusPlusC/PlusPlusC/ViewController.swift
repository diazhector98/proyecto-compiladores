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
    }
    
    @IBAction func runButtonPressed(_ sender: Any) {
    }
    
    
    
    
}

