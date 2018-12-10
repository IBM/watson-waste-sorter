//
//  ViewController.swift
//  Watson Waste Sorter
//
//  Created by XiaoguangMo on 12/4/17.
//  Copyright © 2017 IBM Inc. All rights reserved.
//

import UIKit
import Alamofire
import CameraManager
import SimpleAlert
import NVActivityIndicatorView

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    @IBOutlet weak var loadingView: NVActivityIndicatorView!
    @IBOutlet weak var main: UIView!
    @IBOutlet weak var shoot: UIImageView!
    var myImage: UIImage!
    let cameraManager = CameraManager()
    let SERVER_API_ENDPOINT = Bundle.main.infoDictionary!["SERVER_API_ENDPOINT"] as! String
    override func viewDidLoad() {
        super.viewDidLoad()
        cameraManager.addPreviewLayerToView(self.main)
        cameraManager.cameraOutputQuality = .medium

    }

    @IBAction func takePhoto(_ sender: Any) {
        if loadingView.animating {
            return
        }
        self.loadingView.startAnimating()
        self.view.bringSubview(toFront: loadingView)
        main.bringSubview(toFront: loadingView)
        cameraManager.capturePictureWithCompletion({ (image, error) -> Void in
            self.myImage = image
            let imageData = UIImageJPEGRepresentation(image!, 1)!
            Alamofire.upload(
                multipartFormData: { multipartFormData in
                    multipartFormData.append(imageData, withName: "images_file", fileName: "image.jpg", mimeType: "image/jpg")
            },
                to: self.SERVER_API_ENDPOINT,
                encodingCompletion: { encodingResult in
                    switch encodingResult {
                    case .success(let upload, _, _):
                        upload.responseJSON { response in
                            if let status = response.response?.statusCode {
                                switch(status){
                                case 200:
                                    if let result = response.result.value {
                                        let JSON = result as! NSDictionary
                                        print(JSON)
                                        if let res = JSON["result"] as? String {
                                            if let confs = JSON["confident score"] as? Double {
                                                self.showAlert(text: res, conf:Int(confs * 100))
                                            }
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

    func showAlert(text:String, conf:Int) {
        var res = text
        if res == "Image is either not a waste or it's too blurry, please try it again."{
            res = "Unclassified"
        }
        let alert = AlertController(view: UIView(), style: .alert)
        alert.contentWidth = 200
        alert.contentCornerRadius = 100
        alert.contentColor = .white
        let action = AlertAction(title: "\(res)", style: .cancel) { action in
        }
        let confView = UILabel(frame:CGRect(x: 0, y: 125, width: 200, height: 21))
        confView.text = "Confident Score: \(conf)%"
        confView.font = UIFont(name: "Halvetica", size: 15)
        confView.textAlignment = .center
        action.button.addSubview(confView)
        action.button.bringSubview(toFront: confView)
        alert.addAction(action)
        action.button.frame.size.height = 200
        action.button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 30)
        switch(res){
        case "Unclassified":
            action.button.setTitleColor(UIColor.red, for: .normal)
        case "Landfill":
            action.button.setTitleColor(UIColor.black, for: .normal)
        case "Compost":
            action.button.setTitleColor(UIColor.green, for: .normal)
        default:
            action.button.setTitleColor(UIColor.blue, for: .normal)
        }


        self.loadingView.stopAnimating()
        self.present(alert, animated: true, completion: nil)
    }
    // MARK: - UIImagePickerControllerDelegate Methods

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}
