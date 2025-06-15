package com.ael.productservice.service.impl;

import com.ael.productservice.dto.request.ProductRequest;
import com.ael.productservice.dto.request.ProductUpdateRequest;
import com.ael.productservice.dto.response.ProductCreateResponse;
import com.ael.productservice.dto.response.ProductGetAllResponse;
import com.ael.productservice.dto.response.ProductUnitResponse;
import com.ael.productservice.dto.response.ProductUpdateResponse;
import com.ael.productservice.model.Product;
import com.ael.productservice.model.SubCategory;
import com.ael.productservice.repository.IProductRepository;
import com.ael.productservice.repository.ISubCategoryRepository;
import com.ael.productservice.service.abstracts.IProductService;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.BeanWrapper;
import org.springframework.beans.BeanWrapperImpl;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class ProductService implements IProductService {

    private final IProductRepository productRepository;
    private final ISubCategoryRepository subCategoryRepository;

    // Null olmayan alanları getiren yardımcı metod
    private String[] getNullPropertyNames(Object source) {
        final BeanWrapper src = new BeanWrapperImpl(source);
        java.beans.PropertyDescriptor[] pds = src.getPropertyDescriptors();

        Set<String> emptyNames = new HashSet<>();
        for (java.beans.PropertyDescriptor pd : pds) {
            Object srcValue = src.getPropertyValue(pd.getName());
            if (srcValue == null) emptyNames.add(pd.getName());
        }
        String[] result = new String[emptyNames.size()];
        return emptyNames.toArray(result);
    }

    @Override
    public ProductCreateResponse createProduct(ProductRequest productRequest) {
        try {

            SubCategory subCategory = subCategoryRepository.findById(productRequest.getSubCategoryId()).orElseThrow(()->new RuntimeException("SubCategory not found"));

            Product newProduct = Product.builder()
                    .productDescription(productRequest.getProductDescription())
                    .productName(productRequest.getProductName())
                    .productPrice(productRequest.getProductPrice())
                    .productQuantity(productRequest.getProductQuantity())
                    .subcategory(subCategory).build();

            productRepository.save(newProduct);

            return ProductCreateResponse.builder()
                    .message("Product created")
                    .build();

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return null;
    }

    @Override
    public List<ProductGetAllResponse> getAllProducts() {
        // Product listesi al
        List<Product> products = productRepository.findAll();

        // Product listesini ProductGetAllResponse DTO listesine dönüştür
        List<ProductGetAllResponse> response = products.stream()
                .map(product -> {
                    ProductGetAllResponse dto = new ProductGetAllResponse();
                    dto.setProductId(product.getProductId());
                    dto.setProductName(product.getProductName());
                    dto.setProductDescription(product.getProductDescription());
                    dto.setProductPrice(product.getProductPrice());
                    dto.setProductQuantity(product.getProductQuantity());
                    dto.setSubCategoryId(product.getSubcategory().getSubCategoryId()); // SubCategoryId'yi al
                    return dto;
                })
                .collect(Collectors.toList());

        return response;
    }

    @Override
    public ProductUnitResponse getProduct(Integer productId) {

        Product product = productRepository.findById(productId).orElseThrow(()->new RuntimeException("Product not found"));

        return  ProductUnitResponse.builder()
                .productName(product.getProductName())
                .productDescription(product.getProductDescription())
                .productPrice(product.getProductPrice())
                .productId(product.getProductId())
                .subCategoryName(product.getSubcategory().getSubCategoryName())
                .subCategoryId(product.getSubcategory().getSubCategoryId())
                .build();


    }

    @Override
    public ProductUpdateResponse updateProduct(Integer productId, ProductUpdateRequest productUpdateRequest) {
        try {
            // Ürünü veritabanından bul
            Product existingProduct = productRepository.findById(productId)
                    .orElseThrow(() -> new RuntimeException("Product not found with id: " + productId));

            // SubCategory kontrolü (eğer subCategoryId gönderilmişse)
            if (productUpdateRequest.getSubCategoryId() != null) {
                SubCategory subCategory = subCategoryRepository.findById(productUpdateRequest.getSubCategoryId())
                        .orElseThrow(() -> new RuntimeException("SubCategory not found with id: " + productUpdateRequest.getSubCategoryId()));
                existingProduct.setSubcategory(subCategory);
            }

            // Null olmayan alanları kopyala (sadece değişiklikler uygulanır)
            BeanUtils.copyProperties(productUpdateRequest, existingProduct, getNullPropertyNames(productUpdateRequest));

            // Güncellenmiş ürünü kaydet
            Product updatedProduct = productRepository.save(existingProduct);

            // Response DTO'sunu oluştur
            return ProductUpdateResponse.builder()
                    .message("Product updated successfully")
                    .productId(updatedProduct.getProductId())
                    .productName(updatedProduct.getProductName())
                    .productDescription(updatedProduct.getProductDescription())
                    .productPrice(updatedProduct.getProductPrice())
                    .productQuantity(updatedProduct.getProductQuantity())
                    .subCategoryId(updatedProduct.getSubcategory().getSubCategoryId())
                    .subCategoryName(updatedProduct.getSubcategory().getSubCategoryName())
                    .build();

        } catch (Exception e) {
            System.out.println("Error updating product: " + e.getMessage());
            throw new RuntimeException("Failed to update product: " + e.getMessage());
        }
    }
}
