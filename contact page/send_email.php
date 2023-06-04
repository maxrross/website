<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST['name'];
  $email = $_POST['email'];
  $major = $_POST['major'];
  $schoolYear = $_POST['school-year'];
  $contactReason = $_POST['contact-reason'];
  $message = $_POST['message'];

  // Set up the email parameters
  $to = 'yingyingzhang1@ufl.edu'; // Replace with your email address
  $subject = 'New Contact Form Submission';
  $headers = "From: $email\r\n";
  $headers .= "Reply-To: $email\r\n";
  $messageBody = "Name: $name\n";
  $messageBody .= "Email: $email\n";
  $messageBody .= "Major: $major\n";
  $messageBody .= "School Year: $schoolYear\n";
  $messageBody .= "Reason for Contact: $contactReason\n";
  $messageBody .= "Message: $message\n";

  // Send the email
  $mailSent = mail($to, $subject, $messageBody, $headers);

  // Check if the email was sent successfully
  if ($mailSent) {
    echo "Thank you for your message. We'll get back to you soon!";
  } else {
    echo "Oops! Something went wrong. Please try again.";
  }
}
?>
