import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import java.util.Random;

public class ImageProcessingApp {
    static { System.loadLibrary(Core.NATIVE_LIBRARY_NAME); }

    private JFrame frame;
    private JLabel imageLabel;
    private Mat image;

    public ImageProcessingApp() {
        frame = new JFrame("Image Processing Application");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1200, 800);

        JPanel controlPanel = new JPanel();

        JButton loadButton = new JButton("Load Image");
        loadButton.addActionListener(this::loadImage);

        JButton saveButton = new JButton("Save Image");
        saveButton.addActionListener(this::saveImage);

        JButton noiseButton = new JButton("Add Noise");
        noiseButton.addActionListener(e -> addNoise());

        JButton triangleFilterButton = new JButton("Triangle Filter");
        triangleFilterButton.addActionListener(e -> applyTriangleFilter());

        JButton gaussianFilterButton = new JButton("Gaussian Filter");
        gaussianFilterButton.addActionListener(e -> applyGaussianFilter());

        JButton medianFilterButton = new JButton("Median Filter");
        medianFilterButton.addActionListener(e -> applyMedianFilter());

        JButton kuwaharaFilterButton = new JButton("Kuwahara Filter");
        kuwaharaFilterButton.addActionListener(e -> applyKuwaharaFilter());

        JButton manualThresholdButton = new JButton("Manual Threshold");
        manualThresholdButton.addActionListener(e -> applyManualThreshold());

        JButton otsuThresholdButton = new JButton("Otsu's Threshold");
        otsuThresholdButton.addActionListener(e -> applyOtsuThreshold());

        JButton adaptiveThresholdButton = new JButton("Adaptive Threshold");
        adaptiveThresholdButton.addActionListener(e -> applyAdaptiveThreshold());

        controlPanel.add(loadButton);
        controlPanel.add(saveButton);
        controlPanel.add(noiseButton);
        controlPanel.add(triangleFilterButton);
        controlPanel.add(gaussianFilterButton);
        controlPanel.add(medianFilterButton);
        controlPanel.add(kuwaharaFilterButton);
        controlPanel.add(manualThresholdButton);
        controlPanel.add(otsuThresholdButton);
        controlPanel.add(adaptiveThresholdButton);

        imageLabel = new JLabel();
        frame.getContentPane().add(controlPanel, BorderLayout.NORTH);
        frame.getContentPane().add(imageLabel, BorderLayout.CENTER);

        frame.setVisible(true);
    }

    private void loadImage(ActionEvent e) {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new FileNameExtensionFilter("Image Files", "jpg", "png", "bmp"));
        int result = fileChooser.showOpenDialog(frame);
        if (result == JFileChooser.APPROVE_OPTION) {
            image = Imgcodecs.imread(fileChooser.getSelectedFile().getAbsolutePath());
            displayImage(convertMatToImage(image));
        }
    }

    private void saveImage(ActionEvent e) {
        if (image != null) {
            JFileChooser fileChooser = new JFileChooser();
            int result = fileChooser.showSaveDialog(frame);
            if (result == JFileChooser.APPROVE_OPTION) {
                Imgcodecs.imwrite(fileChooser.getSelectedFile().getAbsolutePath(), image);
            }
        }
    }

    private void addNoise() {
        if (image != null) {
            Random rand = new Random();
            for (int i = 0; i < image.rows(); i++) {
                for (int j = 0; j < image.cols(); j++) {
                    double[] pixel = image.get(i, j);
                    if (rand.nextDouble() < 0.1) { // 10% chance of noise
                        pixel[0] = rand.nextInt(256); // B channel
                        pixel[1] = rand.nextInt(256); // G channel
                        pixel[2] = rand.nextInt(256); // R channel
                    }
                    image.put(i, j, pixel);
                }
            }
            displayImage(convertMatToImage(image));
        }
    }

    private void applyTriangleFilter() {
        if (image != null) {
            Mat kernel = Mat.ones(5, 5, CvType.CV_32F);
            Core.divide(kernel, new Scalar(25), kernel); // Normalizing the kernel
            Imgproc.filter2D(image, image, -1, kernel);
            displayImage(convertMatToImage(image));
        }
    }

    private void applyGaussianFilter() {
        if (image != null) {
            Imgproc.GaussianBlur(image, image, new Size(5, 5), 1.5);
            displayImage(convertMatToImage(image));
        }
    }

    private void applyMedianFilter() {
        if (image != null) {
            Imgproc.medianBlur(image, image, 5);
            displayImage(convertMatToImage(image));
        }
    }

    private void applyKuwaharaFilter() {
        if (image != null) {
            Mat result = new Mat(image.size(), image.type());
            for (int i = 2; i < image.rows() - 2; i++) {
                for (int j = 2; j < image.cols() - 2; j++) {
                    // Extract the 5x5 neighborhood
                    Mat submat = image.submat(i - 2, i + 3, j - 2, j + 3);
                    double[] meanPixel = Core.mean(submat).val;
                    result.put(i, j, meanPixel);
                }
            }
            image = result;
            displayImage(convertMatToImage(image));
        }
    }

    private void applyManualThreshold() {
        if (image != null) {
            String input = JOptionPane.showInputDialog("Enter threshold (0-255):");
            int threshold = Integer.parseInt(input);
            Imgproc.threshold(image, image, threshold, 255, Imgproc.THRESH_BINARY);
            displayImage(convertMatToImage(image));
        }
    }

    private void applyOtsuThreshold() {
        if (image != null) {
            Imgproc.cvtColor(image, image, Imgproc.COLOR_BGR2GRAY);
            Imgproc.threshold(image, image, 0, 255, Imgproc.THRESH_BINARY + Imgproc.THRESH_OTSU);
            displayImage(convertMatToImage(image));
        }
    }

    private void applyAdaptiveThreshold() {
        if (image != null) {
            Imgproc.cvtColor(image, image, Imgproc.COLOR_BGR2GRAY);
            Imgproc.adaptiveThreshold(image, image, 255, Imgproc.ADAPTIVE_THRESH_MEAN_C,
                    Imgproc.THRESH_BINARY, 11, 2);
            displayImage(convertMatToImage(image));
        }
    }

    private void displayImage(Image img) {
        imageLabel.setIcon(new ImageIcon(img));
        frame.repaint();
    }

    private Image convertMatToImage(Mat mat) {
        int type = BufferedImage.TYPE_BYTE_GRAY;
        if (mat.channels() > 1) {
            Mat matRGB = new Mat();
            Imgproc.cvtColor(mat, matRGB, Imgproc.COLOR_BGR2RGB);
            mat = matRGB;
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        byte[] b = new byte[mat.rows() * mat.cols() * mat.channels()];
        mat.get(0, 0, b);
        BufferedImage image = new BufferedImage(mat.cols(), mat.rows(), type);
        image.getRaster().setDataElements(0, 0, mat.cols(), mat.rows(), b);
        return image;
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(ImageProcessingApp::new);
    }
}
