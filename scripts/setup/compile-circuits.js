const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execAsync = util.promisify(exec);

/**
 * Circuit compilation script for EquiPath ESP Grant
 * Compiles Circom circuits and generates proving/verification keys
 */

const CIRCUITS_DIR = path.join(__dirname, '../../circuits');
const BUILD_DIR = path.join(CIRCUITS_DIR, 'build');
const VERIFICATION_DIR = path.join(CIRCUITS_DIR, 'verification');

// Circuit configuration
const CIRCUITS = [
    {
        name: 'knowledge_verification',
        input: path.join(VERIFICATION_DIR, 'knowledge_verification.circom'),
        output: path.join(BUILD_DIR, 'knowledge_verification')
    }
];

async function ensureDirectories() {
    console.log('📁 Creating build directories...');
    
    if (!fs.existsSync(BUILD_DIR)) {
        fs.mkdirSync(BUILD_DIR, { recursive: true });
        console.log('✅ Created build directory');
    }
    
    if (!fs.existsSync(path.join(BUILD_DIR, 'keys'))) {
        fs.mkdirSync(path.join(BUILD_DIR, 'keys'), { recursive: true });
        console.log('✅ Created keys directory');
    }
}

async function compileCircuit(circuit) {
    console.log(`🔧 Compiling circuit: ${circuit.name}`);
    
    try {
        // Compile circuit to R1CS, WASM, and SYM
        const compileCmd = `circom ${circuit.input} --r1cs --wasm --sym -o ${BUILD_DIR}`;
        console.log(`Running: ${compileCmd}`);
        
        const { stdout, stderr } = await execAsync(compileCmd);
        
        if (stderr && !stderr.includes('Written successfully')) {
            console.warn('⚠️  Compilation warnings:', stderr);
        }
        
        console.log('✅ Circuit compiled successfully');
        console.log(stdout);
        
        return true;
    } catch (error) {
        console.error(`❌ Failed to compile circuit ${circuit.name}:`, error.message);
        return false;
    }
}

async function generateKeys(circuit) {
    console.log(`🔑 Generating proving and verification keys for: ${circuit.name}`);
    
    const r1csPath = path.join(BUILD_DIR, `${circuit.name}.r1cs`);
    const ptauPath = path.join(BUILD_DIR, 'keys', 'powersoftau.ptau');
    const zkeyPath = path.join(BUILD_DIR, 'keys', `${circuit.name}.zkey`);
    const vkeyPath = path.join(BUILD_DIR, 'keys', `${circuit.name}_vkey.json`);
    
    try {
        // Generate powers of tau (small ceremony for testing)
        if (!fs.existsSync(ptauPath)) {
            console.log('🌟 Generating powers of tau...');
            await execAsync(`snarkjs powersoftau new bn128 12 ${ptauPath} -v`);
            await execAsync(`snarkjs powersoftau prepare phase2 ${ptauPath} ${ptauPath} -v`);
            console.log('✅ Powers of tau generated');
        }
        
        // Generate zkey
        console.log('🔐 Generating proving key...');
        await execAsync(`snarkjs groth16 setup ${r1csPath} ${ptauPath} ${zkeyPath}`);
        console.log('✅ Proving key generated');
        
        // Export verification key
        console.log('🔓 Exporting verification key...');
        await execAsync(`snarkjs zkey export verificationkey ${zkeyPath} ${vkeyPath}`);
        console.log('✅ Verification key exported');
        
        return true;
    } catch (error) {
        console.error(`❌ Failed to generate keys for ${circuit.name}:`, error.message);
        return false;
    }
}

async function verifySetup(circuit) {
    console.log(`🔍 Verifying setup for: ${circuit.name}`);
    
    const wasmPath = path.join(BUILD_DIR, `${circuit.name}_js`, `${circuit.name}.wasm`);
    const zkeyPath = path.join(BUILD_DIR, 'keys', `${circuit.name}.zkey`);
    const vkeyPath = path.join(BUILD_DIR, 'keys', `${circuit.name}_vkey.json`);
    
    const filesExist = [
        fs.existsSync(wasmPath),
        fs.existsSync(zkeyPath),
        fs.existsSync(vkeyPath)
    ];
    
    if (filesExist.every(exists => exists)) {
        console.log('✅ All circuit files generated successfully');
        console.log(`   WASM: ${wasmPath}`);
        console.log(`   Proving Key: ${zkeyPath}`);
        console.log(`   Verification Key: ${vkeyPath}`);
        return true;
    } else {
        console.log('❌ Some circuit files are missing');
        return false;
    }
}

async function main() {
    console.log('🚀 Starting EquiPath Circuit Compilation');
    console.log('=====================================');
    
    try {
        // Ensure directories exist
        await ensureDirectories();
        
        let allSuccessful = true;
        
        // Process each circuit
        for (const circuit of CIRCUITS) {
            console.log(`\n📋 Processing circuit: ${circuit.name}`);
            console.log('-----------------------------------');
            
            // Compile circuit
            const compiled = await compileCircuit(circuit);
            if (!compiled) {
                allSuccessful = false;
                continue;
            }
            
            // Generate keys
            const keysGenerated = await generateKeys(circuit);
            if (!keysGenerated) {
                allSuccessful = false;
                continue;
            }
            
            // Verify setup
            const verified = await verifySetup(circuit);
            if (!verified) {
                allSuccessful = false;
            }
        }
        
        console.log('\n🎉 Circuit Compilation Summary');
        console.log('==============================');
        
        if (allSuccessful) {
            console.log('✅ All circuits compiled successfully!');
            console.log('✅ Proving and verification keys generated');
            console.log('✅ EquiPath is ready for zk-SNARK proof generation');
            console.log('\nNext steps:');
            console.log('1. Run: npm test');
            console.log('2. Test proof generation with your SDK');
        } else {
            console.log('❌ Some circuits failed to compile');
            console.log('Please check the error messages above');
            process.exit(1);
        }
        
    } catch (error) {
        console.error('❌ Compilation process failed:', error.message);
        process.exit(1);
    }
}

// Run the compilation
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { main, compileCircuit, generateKeys };
