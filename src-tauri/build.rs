use std::env;
use std::fs;
use std::path::Path;

fn main() {
    tauri_build::build();
    
    // Copy Python files and templates to the bundle
    let out_dir = env::var("OUT_DIR").unwrap();
    let manifest_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    let project_root = Path::new(&manifest_dir).parent().unwrap();
    
    // Create resources directory
    let resources_dir = Path::new(&out_dir).join("resources");
    fs::create_dir_all(&resources_dir).unwrap();
    
    // Copy Python files
    let python_files = ["web_lyricstamp.py", "player_control.py", "ai_postprocess.py"];
    for file in &python_files {
        let src = project_root.join(file);
        let dst = resources_dir.join(file);
        if src.exists() {
            fs::copy(&src, &dst).unwrap();
        }
    }
    
    // Copy templates directory
    let templates_src = project_root.join("templates");
    let templates_dst = resources_dir.join("templates");
    if templates_src.exists() {
        copy_dir_all(&templates_src, &templates_dst).unwrap();
    }
    
    // Copy requirements.txt
    let requirements_src = project_root.join("requirements.txt");
    let requirements_dst = resources_dir.join("requirements.txt");
    if requirements_src.exists() {
        fs::copy(&requirements_src, &requirements_dst).unwrap();
    }
}

fn copy_dir_all(src: &Path, dst: &Path) -> std::io::Result<()> {
    if !dst.exists() {
        fs::create_dir(dst)?;
    }
    
    for entry in fs::read_dir(src)? {
        let entry = entry?;
        let ty = entry.file_type()?;
        let src_path = entry.path();
        let dst_path = dst.join(entry.file_name());
        
        if ty.is_dir() {
            copy_dir_all(&src_path, &dst_path)?;
        } else {
            fs::copy(&src_path, &dst_path)?;
        }
    }
    Ok(())
} 