//
//  ViewController.swift
//  Watson Waste Sorter
//
//  Created by XiaoguangMo on 12/4/17.
//  Copyright © 2017 XiaoguangMo. All rights reserved.
//

import UIKit
import Alamofire
import CameraManager
import SimpleAlert

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var main: UIView!
    @IBOutlet weak var shoot: UIImageView!
    var myImage: UIImage!
    let cameraManager = CameraManager()
    override func viewDidLoad() {
        super.viewDidLoad()
        cameraManager.addPreviewLayerToView(self.main)
        cameraManager.cameraOutputQuality = .medium
        
    }

    @IBAction func takePhoto(_ sender: Any) {
        cameraManager.capturePictureWithCompletion({ (image, error) -> Void in
            self.myImage = image
            let imageData = UIImageJPEGRepresentation(image!, 1)!
            Alamofire.upload(
                multipartFormData: { multipartFormData in
                    multipartFormData.append(imageData, withName: "images_file", fileName: "image.jpg", mimeType: "image/jpg")
            },
                to: "https://watson-waste-sorter.mybluemix.net/api/sort",
                encodingCompletion: { encodingResult in
                    switch encodingResult {
                    case .success(let upload, _, _):
                        upload.responseJSON { response in
                            if let status = response.response?.statusCode {
                                switch(status){
                                case 200:
                                    if let result = response.result.value {
                                        let JSON = result as! NSDictionary
                                        if let res = JSON["result"] as? String {
                                            self.showAlert(text: res)
                                        }
                                    }
                                default:
                                    print("error with response status: \(status)")
                                }
                            }
                            
//                            debugPrint(response)
//                            print(response.description)
                        }
                    case .failure(let encodingError):
                        print(encodingError)
                    }
            }
            )
        })
    }
    
    func showAlert(text:String) {
        var res = text
        if res == "Image is either not a waste or it's too blurry, please try it again."{
            res = "Unclassified"
        }
        let alert = AlertController(view: UIView(), style: .alert)
        alert.contentWidth = 144
        alert.contentCornerRadius = 72
        alert.contentColor = .white
        let action = AlertAction(title: "\(res)", style: .cancel) { action in
        }
        
        alert.addAction(action)
        switch(res){
        case "Unclassified":
            action.button.frame.size.height = 144
            action.button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 20)
            action.button.setTitleColor(UIColor.red, for: .normal)
        case "Landfill":
            action.button.frame.size.height = 144
            action.button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 30)
            action.button.setTitleColor(UIColor.black, for: .normal)
        case "Compost":
            action.button.frame.size.height = 144
            action.button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 30)
            action.button.setTitleColor(UIColor.green, for: .normal)
        default:
            action.button.frame.size.height = 144
            action.button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 30)
            action.button.setTitleColor(UIColor.blue, for: .normal)
        }
        
        self.present(alert, animated: true, completion: nil)
        print(res)
    }
    // MARK: - UIImagePickerControllerDelegate Methods
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

