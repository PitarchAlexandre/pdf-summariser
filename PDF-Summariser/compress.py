
"In cas if I have to compress a file."
@staticmethod
def compress_pdf_file(pdf_file):
        # Open document
        document = ap.Document(pdf_file)
        # Initialize OptimizationOptions
        optimizeOptions = ap.optimization.OptimizationOptions()
        # Set CompressImages option
        optimizeOptions.image_compression_options.compress_images = True
        # Set ImageQuality option
        optimizeOptions.image_compression_options.image_quality = 10
        # Removes unused objects
        optimizeOptions.remove_unused_objects = True
        # Link objects in double
        optimizeOptions.link_duplicate_streams = True
        # Optimize PDF document using OptimizationOptions
        document.optimize_resources(optimizeOptions)
        # Save updated document
        out_put = document.save(pdf_file)
        return out_put
